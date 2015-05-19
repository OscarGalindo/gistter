from datetime import datetime
import mongokit


class Core(mongokit.Document):
    __database__ = "gistter"
    use_dot_notation = True
    raise_validation_errors = False
    structure = {
        "created_at": datetime,
        "updated_at": datetime
    }

    default_values = {
        "created_at": datetime.utcnow,
        "updated_at": datetime.utcnow
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super(Core, self).save(*args, **kwargs)