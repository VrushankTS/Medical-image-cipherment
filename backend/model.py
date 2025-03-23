import torch
import torch.nn as nn


class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.relu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.relu(out)
        out = self.conv2(out)
        out += residual
        return out


class FeatureEncoderModule(nn.Module):
    def __init__(self, in_channels=1, out_channels=64, num_res_blocks=4):
        super(FeatureEncoderModule, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1)
        self.res_blocks = nn.Sequential(*[ResidualBlock(out_channels) for _ in range(num_res_blocks)])
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=2, padding=1)
        self.relu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.res_blocks(x)
        x = self.conv2(x)
        return x


class FeatureDecoderModule(nn.Module):
    def __init__(self, in_channels=64, out_channels=1, num_res_blocks=4):
        super(FeatureDecoderModule, self).__init__()
        self.conv1 = nn.ConvTranspose2d(in_channels, in_channels, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.res_blocks = nn.Sequential(*[ResidualBlock(in_channels) for _ in range(num_res_blocks)])
        self.conv2 = nn.ConvTranspose2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.relu = nn.LeakyReLU(0.2, inplace=True)
        self.output_activation = nn.Sigmoid()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.res_blocks(x)
        x = self.conv2(x)
        x = self.output_activation(x)
        return x
    

class FeatureFusionPassingModule(nn.Module):
    def __init__(self, channels):
        super(FeatureFusionPassingModule, self).__init__()
        self.res_block1 = ResidualBlock(channels)
        self.res_block2 = ResidualBlock(channels)
        self.res_block3 = ResidualBlock(channels)

    def forward(self, Fi, Ki):
        alpha_i = torch.sigmoid(self.res_block1(Fi))  # Learnable fusion parameter
        Fi_next = alpha_i * Fi + (1 - alpha_i) * Ki  # Dynamic feature fusion
        Fi_next = self.res_block2(Fi_next)
        Fi_next = self.res_block3(Fi_next)
        return Fi_next
    

class FeatureFusionEncryptionModule(nn.Module):
    def __init__(self, channels):
        super(FeatureFusionEncryptionModule, self).__init__()
        self.F_block = ResidualBlock(channels)  # Function F
        self.G_block = ResidualBlock(channels)  # Function G

    def forward(self, Ki, alpha_i):
        EKi = Ki + self.F_block(alpha_i)  # Encrypted Key
        EPi = alpha_i + self.G_block(EKi)  # Encrypted Feature
        print("Original Key (Ki):", Ki)
        print("Encrypted Key (EKi):", EKi)
        print("Fusion Parameter (alpha_i):", alpha_i)
        print("Encrypted Feature (EPi):", EPi)
        return EKi, EPi
    

class FeatureFusionDecryptionModule(nn.Module):
    def __init__(self, channels):
        super(FeatureFusionDecryptionModule, self).__init__()
        self.F_block = ResidualBlock(channels)  # Function F
        self.G_block = ResidualBlock(channels)  # Function G

    def forward(self, EKi, EPi):
        alpha_i = EPi - self.G_block(EKi)  # Recover alpha
        Ki = EKi - self.F_block(alpha_i)  # Recover feature key
        print("Recovered Fusion Parameter (alpha_i):", alpha_i)
        print("Recovered Key (Ki):", Ki)
        return Ki, alpha_i
    

class MedicalImageEncryptionModel(nn.Module):
    def __init__(self, channels=64):
        super(MedicalImageEncryptionModel, self).__init__()
        self.encoder = FeatureEncoderModule()
        self.encryption = FeatureFusionEncryptionModule(channels)
        self.decryption = FeatureFusionDecryptionModule(channels)
        self.decoder = FeatureDecoderModule()

    def forward(self, x):
        # Step 1: Encode Image Features
        Ki = self.encoder(x)

        # Step 2: Generate a random fusion parameter alpha_i (same shape as Ki)
        alpha_i = torch.rand_like(Ki, device=Ki.device)

        # Step 3: Encrypt Features
        EKi, EPi = self.encryption(Ki, alpha_i)

        # Step 4: Decrypt Features
        recovered_Ki, recovered_alpha_i = self.decryption(EKi, EPi)

        # Step 5: Decode the Recovered Features
        reconstructed_x = self.decoder(recovered_Ki)

        return reconstructed_x, Ki, EKi, EPi, recovered_Ki