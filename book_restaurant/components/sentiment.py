from __future__ import annotations

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.engine.recipes.default_recipe import DefaultV1Recipe

from typing import List, Type, Dict, Text, Any, Optional

from rasa.engine.graph import ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage

from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.constants import TEXT

from rasa.nlu.extractors.extractor import EntityExtractorMixin

from nltk.sentiment.vader import SentimentIntensityAnalyzer


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR, is_trainable=False
)

class SentimentAnalyzer(GraphComponent, EntityExtractorMixin):
   
    """A pre-trained sentiment component"""

    name = "sentiment"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config: Dict[Text, Any]) -> None:

        self.component_config = component_config

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config)

    def train(self, training_data: TrainingData) -> Resource:
        pass

    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "sentiment_extractor"}

        return entity

    def process(self, messages: List[Message]) -> List[Message]:
        """Retrieve the text message, pass it to the classifier and append the prediction results 
        to the message class."""
        sid = SentimentIntensityAnalyzer()
        for message in messages:
            res = sid.polarity_scores(message.get(TEXT))
            #key, value = max(res.items(), key=lambda x: x[1])
            #entity = self.convert_to_rasa(key, value)
            entities = []
            for r in res:
                entity = self.convert_to_rasa(r, res[r])
                entities.append(entity)
            # Create a specific entity 'user_unhappy' for a slot with the same name.
            # This slot can then influence the conversation.
            if res['compound'] < -0.2:
                entity = self.convert_to_rasa("user_unhappy", True)
                entities.append(entity)
            message.set("entities", entities, add_to_output=True)

        return messages

    def persist(self, file_name, model_dir):
        """Pass because a pre-trained model is already persisted"""
        pass