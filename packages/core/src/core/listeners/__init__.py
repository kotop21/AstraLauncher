import core.listeners.server

from .test_listener import TestListener
from .open_folder import OpenFolderListener
from .user_file_manager_listener import UserFileManagerListener
from .dialog import DialogListener

test = TestListener()
open_folder = OpenFolderListener()
user_file_manager = UserFileManagerListener()
dialog = DialogListener()
