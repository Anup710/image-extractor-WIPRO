## Wipro-Columbus Computer vision based classifier

The purpose of this repo is to experiment various approaches for building an AI application which classifies existing component drawings and extracts key dimensions. 

There are 2 appraoches primarily:

1. Using smaller open source model

- Models under contention: Qwen2-VL-72B, InternVL2-76B, LLaVA-NeXT-34B, CogVLM2-19B, Llava-7B

__Results observed__: Performance of baseline 7B model is terrible (wrong component identification ex. piston identified as seal) and dimensions are being hallucinated. 

__Next Steps__: Use bigger models or ones better at (technical) vision based tasks. Maximize prompt engineering and then proceed to mini SFT by preparing synthetic labelled data. (like instruction fine tuning). Its anyones guess on _how_ SFT will perform, not considering expertise and compute required to perform it. 

2. Using api based SOTA models

- Establish baseline performance using a simple prompt
- Experiment with prompt engineering since baseline performance is quite good as is
- Niche models such as GPT-4Vision or Gemini 2.5-pro could improve performance

__Results observed__: GPT-5 or Claude-4 give pretty accurate results in one shot. The dimension extraction is near perfect however labelling is a bit off. (Chamfers, diameters etc.)