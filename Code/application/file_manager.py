import pickle
from typing import Iterable

from sklearn.preprocessing import LabelBinarizer
import os
import sys
import shutil
from tensorflow.keras.models import load_model
from pathlib import Path

class file_manager:
    def __init__(self):
        if getattr(sys, 'frozen', False):  # running in PyInstaller bundle
            self.parent_dir = Path(sys._MEIPASS).resolve()
        else:  # running in Python interpreter
            self.parent_dir = Path(__file__).resolve().parents[2]
        for p in (
            self.settings_path,
            self.batches_path,
            self.predictions_path,
            self.storage_path,
            self.page_path
        ):
            p.mkdir(parents=True, exist_ok=True)

    @property
    def settings_path(self) -> Path:
        return self.parent_dir / "Settings"
        # ideally user_config_path for text files but for pickles data_path is
        # good for now

    @property
    def batches_path(self) -> Path:
        return self.parent_dir / "Batches"

    @property
    def predictions_path(self) -> Path:
        return self.parent_dir / "Predictions"

    @property
    def storage_path(self) -> Path:
        return self.parent_dir / "Storage"

    @property
    def page_path(self) -> Path:
        return self.parent_dir / "Pages"

    def save_shorthand(self, shorthand):
        path = self.settings_path / 'shorthand.pkl'
        pickle.dump(shorthand, open(path, 'wb+'))

    def load_shorthand(self):
        shorthand = {}
        path = self.settings_path / 'shorthand.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as sh_load:
                shorthand = pickle.load(sh_load)
    
        return shorthand

    def save_ignore(self, ignore):
        path = self.settings_path / 'ignore.pkl'
        pickle.dump(ignore, open(path, 'wb+'))

    def load_ignore(self):
        ignore = []
        path = self.settings_path / 'ignore.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as ig_load:
                ignore = pickle.load(ig_load)
            
        return ignore

    def save_default_directory(self, default_directory):
        path = self.settings_path / 'default_directory.pkl'
        pickle.dump(default_directory, open(path, 'wb+'))

    def load_default_directory(self):
        default_directory = ''
        path = self.settings_path / 'default_directory.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as dd_load:
                default_directory = pickle.load(dd_load)

        return default_directory

    def save_rows_columns(self, rows_columns):
        path = self.settings_path / 'rows_columns.pkl'
        pickle.dump(rows_columns, open(path, 'wb+'))

    def load_rows_columns(self):
        rows_columns = []
        path = self.settings_path / 'rows_columns.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as rc_load:
                rows_columns = pickle.load(rc_load)

        return rows_columns

    def save_line_thickness(self, line_thickness):
        path = self.settings_path / 'line_thickness.pkl'
        pickle.dump(line_thickness, open(path, 'wb+'))

    def load_line_thickness(self):
        line_thickness = "2"
        path = self.settings_path / 'line_thickness.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as lt_load:
                line_thickness = pickle.load(lt_load)

        return line_thickness

    def save_find_shorthand_matches(self, find_shorthand_matches):
        path = self.settings_path / 'find_shorthand_matches.pkl'
        pickle.dump(find_shorthand_matches, open(path, 'wb+'))

    def load_find_shorthand_matches(self):
        find_shorthand_matches = 0
        path = self.settings_path / 'find_shorthand_matches.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as fsm_load:
                find_shorthand_matches = pickle.load(fsm_load)

        return find_shorthand_matches

    def save_batch(self, batch, batch_num):
        path = self.batches_path / f"batch_{batch_num}"
        pickle.dump(batch, open(path, 'wb+'))

    def load_batch(self, batch_num):
        batch = []
        path = self.batches_path / f"batch_{batch_num}"
        if(os.path.isfile(path)):
            with open(path, 'rb') as batch_load:
                batch = pickle.load(batch_load)

        return batch

    def clear_batches(self):
        folder = self.batches_path
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def save_prediction_results(self, predictions, result_num):
        path = self.predictions_path / f"predictions_{result_num}"
        pickle.dump(predictions, open(path, 'wb+'))

    def load_prediction_results(self, result_num):
        predictions = []
        path = self.predictions_path / f"predictions_{result_num}"
        if(os.path.isfile(path)):
            with open(path, 'rb') as result_load:
                predictions = pickle.load(result_load)

        return predictions

    def clear_results(self):
        folder = self.predictions_path
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def load_LabelBinarizer(self):
        LB = LabelBinarizer()
        path = self.parent_dir / 'LabelBinarizer' / 'LabelBinarizer.pkl'
        with open(path, 'rb') as LB_config:
            LB = pickle.load(LB_config)

        return LB

    def load_ocr_model(self):
        path = self.parent_dir / "Model"
        model = load_model(path)
        return model

    def clear_storage(self):
        folder = self.storage_path
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
            
    def get_storage(self):
        folder = self.storage_path
        filenames = self.sort_storage([f for f in folder.iterdir()])
        return [str(f) for f in filenames]

    def sort_storage(self, filenames: Iterable[Path]):
        return sorted(filenames,
               key=lambda f: int(f.stem))

    def delete_ignored_rows(self):
        ignore = []
        ignore = self.load_ignore()
        rows_columns = []
        rows_columns = self.load_rows_columns()
        for page, row in ignore:
            start_cell = (int(page) - 1)*int(rows_columns[0])*int(rows_columns[1]) + (int(row) - 1)*int(rows_columns[1])
            stop_cell = start_cell + int(rows_columns[1])
            self.delete_cells_in_range(start_cell, stop_cell)

    def delete_cells_in_range(self, start_cell, stop_cell):
        folder = self.storage_path
        for i in range(start_cell, stop_cell):
            filename = str(i) + ".jpg"
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        
