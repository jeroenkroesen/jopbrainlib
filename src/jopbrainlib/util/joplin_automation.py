"""Higher level general functions for interaction with the API
"""

from typing import Dict, Any
#from pydantic import BaseModel
from joppylib import JoplinClient


def ensure_unique_title_notebook(
    joplin: JoplinClient,
    notebook_title: str,
    parent_id: str
) -> Dict[str,Any]:
    """Make sure exactly 1 notebook with notebook_title exists
    """
    fields = ['id', 'title', 'parent_id'] # Fields to return from Joplin search
    search = joplin.folder.search(notebook_title, fields=fields) # search
    if len(search['data']) == 1:
        # Only 1 notebook found - Process further
        if search['data'][0]['title'] == notebook_title and search['data'][0]['parent_id'] == parent_id:
            # Well done, we found the correct notebook. Register the ID
            id = search['data'][0]['id']
        else:
            e = f'Returned note title {search["data"][0]["title"]} does not match {notebook_title}'
            raise ValueError(e)
    elif len(search['data']) > 1:
        # Sad flow: multiple notes returned from search. Exit with error
        e = f'Searching for title {notebook_title} returned more than 1 result.'
        raise ValueError(e)
    else:
        # Happy flow: notebook doesn't exist: create it
        print(f"Notebook {notebook_title} doesn't exist. We need to create it")
        data = {
            'title': notebook_title,
            'parent_id': parent_id
        }
        created_nb = joplin.folder.create(data)
