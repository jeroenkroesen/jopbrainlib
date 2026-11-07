"""Functionality for a diary in Joplin
"""
import pendulum

from typing import List, Optional
from pathlib import Path

from joppylib import JoplinClient

from jopbrainlib.util.datetimes import get_days_in_month
from jopbrainlib.util.templating import get_liquid_env



def create_diary_day(
    joplin: JoplinClient,
    date: pendulum.DateTime, 
    notebook_title: str,
    template_folder: Optional[str] = None,
    body_template_file: str = 'diary_day_body.md',
    title_template_file: str = 'diary_day_title.md'
) -> str:
    """Create a diary note with all required tags for date
    returns the id for the new note.

    To implement later: Deal with multiple entities coming back from search
    results.

    Parameters
    ----------
    joplin : joppylib.JoplinClient
        An authenticated instance of joppylib.JoplinClient
    date : pendulum.DateTime
        The date of the day you want to create a diary not for.
    notebook_title : str
        The title of the notebook you want to create the diary note
        in. The notebook title MUST BE UNIQUE!! If you have multiple 
        notebooks with the same title, create_diary_day() will fail.
    template_folder : str (optional, default: None)
        The str path to the template folder. May contain `~`, `..` and `.`.
        `~` will be resolved to you homefolder and symbolic links will be 
        followed.
    body_template_file : str (default diary_day_body.md)
        Filename of the template for the body of the diary notes. Must end in 
        `.md` and be valid markdown and liquid.
    title_template_file : str (default diary_day_title.md)
        Filename of the template for the title of the diary notes. Must end in 
        `.md` and be valid markdown and liquid.


    Returns
    -------
    id : str
        The Joplin note id of the created note


    Raises
    ------
    FileNotFoundError : if template_folder does not exist in the filesystem.
    """
    # Liquid instantiation
    if not template_folder: # Set default template path
        template_path = Path(__file__).parent.joinpath('templates')
    else:
        template_path = Path(template_folder).expanduser().resolve()
    if not template_path.exists():
        msg = f'template dir {template_path} does not exist.'
        raise FileNotFoundError(msg)
    liquid_env = get_liquid_env(template_path.__str__())
    # Get the id for the notebook diary note should be saved in
    nb_result = joplin.folder.search(notebook_title, ['id'])
    parent_id = nb_result['data'][0]['id']
    # Generate data for the template
    data = {}
    data['year'] = date.format('YYYY')
    data['month_number'] = date.format('MM')
    data['month_name'] = date.format('MMMM').lower()
    data['day_number'] = date.format('DD')
    data['day_name'] = date.format('dddd')
    data['week_nr'] = date.strftime('%V')
    # Load and render templates for body and title
    body_template = liquid_env.get_template(body_template_file)
    title_template = liquid_env.get_template(title_template_file)
    # Render tag names
    tags = []
    tags.append('.diary')
    tags.append(f"time.{data['year']}") # Year. Example: time.2025
    tags.append(f"time.{data['month_name'].lower()}") # Month. Ex: time.february
    tags.append(f"time.week_{data['week_nr']}") # Week. Example: time.week_15
    tags.append(f"time.day_{data['day_number']}") # Day. Example: time.day_16
    # Setup data for creating the note, rendering templates
    note_data = {
        'title': title_template.render(**data).strip(),
        'body': body_template.render(**data),
        'parent_id': parent_id
    }
    # Create the note
    created_note = joplin.note.create(note_data).json()
    # Add the tags to the note
    for tag_title in tags:
        # get id for tag
        tag_found = joplin.tag.search(query=tag_title, fields=['id'])
        # Check if tag exists
        if tag_found['success']:
            tag_id = tag_found['data'][0]['id']
        else:
            # Tag doesn't exist, create it.
            created_tag = joplin.tag.create({'title': tag_title}).json()
            tag_id = created_tag['id']
        joplin.tag.add_to_note(tag_id, created_note['id'])
    return created_note['id']


def create_diary_month(
    joplin: JoplinClient,
    year: int,
    month: int,
    notebook_title: str,
    template_folder: Optional[str] = None,
    body_template_file: str = 'diary_day_body.md',
    title_template_file: str = 'diary_day_title.md'
) -> List[str]:
    """Create a day diary note for each day in the specified month
    """
    month_days = get_days_in_month(year, month)
    month_note_ids = [] # Store created note id's to be returned to caller
    for day in month_days:
        month_note_ids.append(create_diary_day(
            joplin, 
            day, 
            notebook_title,
            template_folder=template_folder,
            body_template_file=body_template_file,
            title_template_file=title_template_file
        ))
    return month_note_ids
