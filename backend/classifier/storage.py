"""
This module contains a custom file storage system to allow files overwriting.
"""
from django.core.files.storage import FileSystemStorage


class OverwriteableStorage(FileSystemStorage):
    """
    Custom file storage to allow files overwriting.

    Notes
    -----
    For further information on how custom file storage works in Django, refer
    to https://docs.djangoproject.com/en/3.2/howto/custom-file-storage
    """

    def _save(self, name, content):
        """
        This method deletes a file called *name* if already exists before
        saving it, which allows the overwriting behaviour.

        Notes
        -----
        For further information on how this method works, refer to
        https://docs.djangoproject.com/en/3.2/howto/custom-file-storage
        """

        self.delete(name)
        return super(OverwriteableStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        """
        This method returns a filename that is available in the storage
        mechanism. Since we want to overwrite the file if already exists, it
        returns the same name as received.

        Notes
        -----
        For further information on how this method works, refer to
        https://docs.djangoproject.com/en/3.2/howto/custom-file-storage
        """

        return name
