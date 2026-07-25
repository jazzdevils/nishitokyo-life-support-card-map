"""
ProgressTracker — tracks geocoding progress across stores via a JSON file.
"""

import json
from pathlib import Path


class ProgressTracker:
    """
    Loads/saves geocoding progress from/to a JSON file.
    Provides the next store index to process and the set of already-processed store IDs.
    """

    def __init__(self, progress_file: str = 'geocoding_progress.json'):
        self.progress_file = Path(progress_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create an empty progress file if it doesn't exist."""
        if not self.progress_file.exists():
            initial = {
                'processed': [],
                'success': 0,
                'fallback': 0,
                'last_processed_id': None,
                'next_store_index': 0
            }
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(initial, f, ensure_ascii=False, indent=2)

    def load(self):
        """Load progress data. Returns (next_index, processed_dict)."""
        with open(self.progress_file, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        processed = {item['id']: item for item in progress['processed']}
        return progress['next_store_index'], processed

    def save(self, processed: dict, next_index: int, total: int):
        """Save progress data from the current run."""
        progress_list = sorted(processed.values(), key=lambda x: x['id'])
        save_data = {
            'processed': progress_list,
            'success': len(progress_list),
            'fallback': 0,
            'last_processed_id': progress_list[-1]['id'] if progress_list else None,
            'next_store_index': next_index
        }
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        print(f'  -> Saved {len(progress_list)}/{total}', flush=True)