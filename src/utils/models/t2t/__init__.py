from .openai_worker import OpenAIWorker
from .llama_worker import LlamaAIWorker
from .base_worker import EmptyScriptException, BaseT2TAIWorker

# Dictionary to pull the specified model implementation at runtime
# keys such as 'openai' are what's to be used as "t2t_ai" value
model_dict = {
    'openai': OpenAIWorker,
    'local': LlamaAIWorker
}
