from typing import List
import dateutil.parser
import datetime
import pytz

from model.Class import Class
from model.Trainer import Trainer

from controller.ClassController import ClassController


class TrainerController:
    def get_current_classes(self, learner_id: int) -> List[Class]:
        """Get Trainer's current classes"""
        all_classes = self.get_all_classes(learner_id)
        current_classes: List[Class] = []
        time_now = datetime.datetime.now(pytz.utc)

        for a_class in all_classes:
            start = dateutil.parser.parse(a_class.class_start_date)
            end = dateutil.parser.parse(a_class.class_end_date)
            if time_now >= start and time_now < end:
                current_classes.append(a_class)

        return current_classes

    def get_future_classes(self, learner_id: int) -> List[Class]:
        """Get Trainer's upcoming/future classes"""
        all_classes = self.get_all_classes(learner_id)
        future_classes: List[Class] = []
        time_now = datetime.datetime.now(pytz.utc)

        for a_class in all_classes:
            start = dateutil.parser.parse(a_class.class_start_date)
            if time_now < start:
                future_classes.append(a_class)

        return future_classes

    def get_past_classes(self, learner_id: int) -> List[Class]:
        """Get Trainer's past classes they taught previously"""
        all_classes = self.get_all_classes(learner_id)
        past_classes: List[Class] = []
        time_now = datetime.datetime.now(pytz.utc)

        for a_class in all_classes:
            end = dateutil.parser.parse(a_class.class_end_date)
            if time_now > end:
                past_classes.append(a_class)

        return past_classes

    def get_all_classes(self, learner_id: int) -> List[Class]:
        all_classes_taught: List[Trainer] = Trainer.query.filter_by(
            user_id=learner_id
        ).all()
        all_classes: List[Class] = []

        for trainer_class in all_classes_taught:
            class_taught: Class = Class.query.filter_by(
                id=trainer_class.class_id
            ).first()
            all_classes.append(class_taught)

        return all_classes

    def get_current_classes_serialise(self, learner_id: int):
        classes = self.get_current_classes(learner_id)
        class_serialise = []
        for aClass in classes:
            class_serialise.append(ClassController().get_class(aClass.id))
        return class_serialise

    def get_future_classes_serialise(self, learner_id: int) -> List[Class]:
        classes = self.get_future_classes(learner_id)
        class_serialise = []
        for aClass in classes:
            class_serialise.append(ClassController().get_class(aClass.id))
        return class_serialise

    def get_past_classes_serialise(self, learner_id: int) -> List[Class]:
        classes = self.get_past_classes(learner_id)
        class_serialise = []
        for aClass in classes:
            class_serialise.append(ClassController().get_class(aClass.id))
        return class_serialise

    def is_trainer(self, learner_id: int) -> bool:
        """Returns true if learner has been assigned to teach a class before"""
        trainer: Trainer = Trainer.query.filter_by(user_id=learner_id).first()
        return trainer != None
