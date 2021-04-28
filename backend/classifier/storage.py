from django.core.files.storage import FileSystemStorage


class OverwriteableStorage(FileSystemStorage):

    def _save(self, name, content):
        self.delete(name)
        return super(OverwriteableStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name
