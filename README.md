# J.A.I.son
[Setup](#setup) | [Training voice](#training-voice) | [Running bot](#running-bot)

## Setup
This was made with Python v3.12.4. It was ran in WSL2 Ubuntu, running an RTX 3070 with the latest drivers installed.

**TO AVOID DEPENDENCY ISSUES FOR LOCAL MODELS, IT IS HIGHLY ADVISED YOU ALSO USED A LINUX BASED ENVIRONMENT**

### Step 1: Before starting
If you intend to run models locally, please ensure you are able to run [CUDA](https://developer.nvidia.com/cuda-toolkit) on you machine and have it installed (this should come with [NVidia drivers](https://www.nvidia.com/en-us/drivers/) by default).

If you don't have the means to run CUDA, then it is advised you use AI services such as [OpenAI](https://platform.openai.com/docs/overview).

### Step 2: Setting up voice
In order to make use of TTS in voice chat as well, you will firstly need something to generate speech.

The following is for old-school TTS generation, and is required whether or not you use it. In Windows, this is built-in with [SAPI5](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ms723627(v=vs.85)). In Linux, you will need to install [eSpeak NG](https://github.com/espeak-ng/espeak-ng/blob/master/docs/guide.md).

The following is for AI TTS generation. It is recommended you use OpenAI services for this once again. This repo currently does not have an option for locally ran TTS AI options, however you may add them by implementing the TTS generation classes.

Lastly, **YOU WILL NEED THE [RVC-PROJECT](https://github.com/limitcantcode/Retrieval-based-Voice-Conversion-WebUI)**. Please refer to ["Training voice"](#training-voice) for more details.

### Step 3: Setting up the VTuber
This project makes use of [VTube Studio](https://denchisoft.com/) to render the VTuber model. After [customizing your VTube model](#customizing-vtuber),you will need to go to `General Settings & External Connections` in settings. First enable the plugins API:

<img src="./assets/vts_2.png" alt="vtube studio plugins panel" height="300"/>

Copy the API adress at the bottom of the panel to be used as `vts_api_address` in your components config. If running on WSL, you will need to replace the IP address (`0.0.0.0` in `ws://0.0.0.0:8001`) with the actual IP address of the computer you are running VTube Studio on (you can simply use your home network IPv4 address, gotten by running `ipconfig` in a Command Prompt and should start with `192.168...`).

Further down, you will need to enable the microphone:

<img src="./assets/vts_1.png" alt="vtube studio microphone panel" height="300"/>

You may select either Simple or Advanced Lipsync, it doesn't matter. If you select Advanced Lipsync, you need to click `Set up in model` (`Ok` on deleting parameters if it asks).

<img src="./assets/vts_3.png" alt="vtube studio set up lipsync" height="300"/>

Before leaving to the next part, pick the microphone input. It is recommended you use a [virtual audio cable](https://vb-audio.com/Cable/) and a [virtual audio mixer](https://vb-audio.com/Voicemeeter/) so you can hear what is being sent to VTube studio. If using VB-Audio (links in previous sentence), unselect all hardware inputs and change the hardware outs to 1. yourself (MME version of device if applicable) and 2. the virtual audio cable INPUT (also MME version). 

<img src="./assets/voicemeter_1.png" alt="voicemeter configuartion" height="400"/>

Back in microphone settings again, select the virtual audio cable OUTPUT. Currently, the audio from the program will be coming from Discord. To send audio into Voicemeeter, navigate to your `Voice & Video settings` and change your `Output Device` to `VoiceMeeter Input...`.

<img src="./assets/discord_2.png" alt="discord audio configuration" height="300"/>

Next, in VTube Studio, go to the `Model Settings` and find paramters for mouth open and mouth form. Change the input to form and open to `VoiceFrequency` and `VoiceVolumn` respectively.

<img src="./assets/vts_4.png" alt="vtube studio model settings" height="500"/>

The first time you run this project, you will need to authenticate some plugins on VTube Studio. A pop-up will automatically appear. Just hit `Allow` on both plugins.

<img src="./assets/vts_7.png" alt="vtube studio plugin auth" height="300"/>

These were just the minimal setup instructions to connect the program to yoour VTube model and sync mouth movement to speaking, however there is still more to do to setup animations and general VTuber movement/expressions. Refer to [Customizing Vtuber](#customizing-vtuber) and [Configuration](#configuration)

### Step 4: Setting up this repo
It is recommended to work from within a virtual python environment. Create one using `python3 -m venv venv` or `python -m venv venv`.
Activate this virtual environment.
```bash
# Windows:
./venv/Scripts/activate
# Linux:
source venv/bin/activate
```

Install the required dependencies.
```bash
pip install -r requirements.txt
```

**IF YOU INSIST ON USING WINDOWS WITH A LOCAL AI,** you will likely need to manually install dependencies for Unsloth. Steps to do so casn be found in [this discussion](https://github.com/unslothai/unsloth/issues/210#issuecomment-1977988036) (the `Home.md` contains the exact instructions at the bottom. I could not get it to work for my hardware, but it may for yours).

Create a `.env` file at the root of this project based on `.env-template`.
You can find you OpenAI API token [here](https://platform.openai.com/api-keys) as shown below:

<img src="./assets/openai_1.png" alt="openai api token location 1" height="200"/>
<img src="./assets/openai_2.png" alt="openai api token location 2" height="200"/>

You can find you Discord Bot token from the [dashboard](https://discord.com/developers/applications) after creating a bot as shown below:

<img src="./assets/discord_1.png" alt="discord bot token location" height="200"/>

Ensure your bot has the right OAuth2 permissions when it joins your server (Scope -> Bot, Bot Permissions -> Administrator if unsure).

## Training T2T
For more on running with custom AI T2T models, refer to the `README.md` in `/scripts` directory.

## Training voice
We don't train direct T2T AI models, but rather AI voice changers using the [RVC-PROJECT](https://github.com/limitcantcode/Retrieval-based-Voice-Conversion-WebUI). You can find a translation of their docs under the `/docs/` directory. Follow the instructions to setup the project, run the web UI, and train a model with you desired voice. **YOU WILL NEED TO BE ABLE TO RUN CUDA TO TRAIN A VOICE**. It is recommended you have a GPU with at least 8GB of dedicated VRAM (not shared or combined with system RAM). If you encounter `CUDA out of memory` errors or something similar, try training smaller models. An RTX 3070 with 8GB or VRAM could only train a v1 model with pitch at 40k sample rate, using both rvmpe_gpu and rvmpe, on a batch size of 1 with no caching. You want to just train a model (be patient after clicking the button, it can take a couple minutes to kick in) and you may ignore training a feature index. If you still have trouble training due to memory, you can swap the pretrained base models from `f0X40k.pth` to just `X40k.pth` where X is either `D` or `G` accordingly.

## Customizing VTuber
This section DOES NOT go over making a model or the basics of how to use VTube Studio (there are plenty of tutorials online). Instead, this section will explain how to get animations and actions from VTube Studio into this project.

Firstly, in VTube Studio, navigate to the `Hotkey Settings & Expressions`. We will add an animation, but the process is the same for expressions and other hotkeyable actions. Here you will find a list of hotkeys and actions:

<img src="./assets/vts_5.png" alt="vtube studio animation hotkey example" height="300"/>

Create as many as you like. Just make sure the name is unique. For each animation, selection `Play Animation...` within `Hotkey Action`, and select the animation you want to play (in my case, `idle1` which for me is in `idle1.motion3.json`). You can create animations by recording yourself performing with `Record Live2D Animation` found at the bottom of `Webcam ... Settings`, or you can create them using Live2D Cubism editor (same one used for making a custom model). Again, there are video tutorials for this.

For our project to use these hotkeys, create a config under `configs/hotkeys`. There are some examples there.

<img src="./assets/vts_6.png" alt="example hotkeys list in vtube studio" height="500"/><img src="./assets/hotkey_config_1.png" alt="example hotkeys config file" height="500"/>

In that same directory is a list of detectable emotions. We map a group of detectable emotions to a group of hotkeys that can potentially be played when that emotion is detected. We refer to each mapping as a "hotkey set". In the above example, we have "hotkey sets" `idle`, `happy`, `agree`, etc (seen on the right). The first "hotkey set" is the set of hotkeys that will be used when idle (not speaking). You may still put emotions in there. Furthermore, **ONLY USE DETECTABLE EMOTIONS ONCE**. That emotion will only be used in the first "hotkey set" listed if it appears in multiple. Detectable emotions go under the `emotions` list while the name of the hotkey goes into the `hotkeys` list.

Your hotkeys are now all setup. To use this hotkey configuration, put the file path to that configuration in your components config file under the key `vts_hotkey_config_file`.

Everytime you run this project and things are setup, you may find the following section in the outputs:

<img src="./assets/hotkey_config_2.png" alt="console output with hotkey debugging" height="400"/>

These are meant to help you see which detectable emotions or existing VTube Studio hotkeys were not included in the config file (`... not assigned`) and which in the config isn't a detectable emotion or VTube Studio hotkey (`... not found`).

## Configuration
Change the values of the config under `./configs` to match your system. `example.json` briefly shows the values that should be there and `default.json` is what I personally used to run this project. Below is a description of the values:

- character_name: (str) Name of your bot and the name it will assume.
- prompt_filepath: (str) Filepath to the prompt text file you want to use. Some may be found under `./prompts`.
- t2t_host: (str) One of `local` or `openai` if you want to run an Unsloth model locally or use OpenAI services respectively.
- t2t_model: (str) Name of OpenAI (checkpoint) model you want to use or name of Unsloth model as you trained it.
- tts_host: (str) One of `old` or `openai` if you want to use old-school TTS synthesis like SAPI or espeak or if you want to use OpenAI's AI TTS service respectively.
- tts_output_filepath: (str) Filepath to where bot should output latest generated TTS. Will be used as intermediate to generate speech initially before converting into desired voice. Requires directory to exist (file doesn't have to exist yet).
- rvc_model: (str) Name of RVC voice model. Is the name you chose when training (so name without the `.pth`).
- rvc_url: (str) URL to your hosted RVC web UI. Typically http://localhost:7865
- rvc_output_filepath: (str) Filepath to where bot should output converted TTS. This is what you finally hear. Requires directory to exist (file doesn't have to exist yet).
- stt_output_filepath: (str) Filepath to most recent audio to be transcribed and sent to t2t.
- vts_api_address: (str) URL to VTube Studio Plugin API. If running from WSL and having issues, refer back to [the top of this section](#step-3-setting-up-the-vtuber)
- server_id: (null or number) Discord server/guild id.

## Running bot
### Step 1: Ensure dependency apps are running
1. Run the RVC-Project (In the same way you [ran the web-UI to train](#training-voice), run the web-UI to start the voice-conversion server using `python ./infer-web.py`)
2. Run Voicemeeter and [configure Discord to output to it's input](#step-3-setting-up-the-vtuber) (instruction halfway down that section)
3. Run VTube Studio with the [Plugin API enabled](#step-3-setting-up-the-vtuber)


### Step 2: Getting the right configuration
Refer to [Configuration](#configuration).

### Step 3: Start running

To run, simply use the following from the project root:
```bash
python ./src/main.py --config=path/to/component_config.json
```