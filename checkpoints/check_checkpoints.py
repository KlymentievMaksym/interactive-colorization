import argparse
import torch

def main():
    parser = argparse.ArgumentParser(description="Check PyTorch Lightning checkpoint")
    parser.add_argument("--ckpt", type=str, default=None, help="File to checkpoint (.ckpt)")
    args = parser.parse_args()

    checkpoint_path = args.ckpt

    print(f"[INFO] Analysing checkpoint: {checkpoint_path}")
    
    try:
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'), weights_only=True)

        epoch = checkpoint.get("epoch")
        global_step = checkpoint.get("global_step")
        hyper_parameters = checkpoint.get("hyper_parameters")
        datamodule_hyper_parameters = checkpoint.get("datamodule_hyper_parameters")

        # print(f"Checkpoint: {checkpoint}")
        print(f"Current Epoch: {epoch} (Starts from 0)")
        print(f"Global Step: {global_step}")
        print(f"Hparams: {hyper_parameters}")
        print(f"Datamodule Hparams: {datamodule_hyper_parameters}")
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {checkpoint_path}")
    except Exception as e:
        print(f"[ERROR] Error reading checkpoint: {e}")

if __name__ == "__main__":
    main()