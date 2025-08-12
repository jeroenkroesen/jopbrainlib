"""Functionality for a diary in Joplin
"""
import pendulum

from typing import List
from collections.abc import Callable

from joppylib.api import Note, Tag, Folder
from joppylib.config import Settings

from jopbrainlib.util.datetimes import get_days_in_month


# JopPyLib instantiation
api_note = Note()
api_tag = Tag()
api_notebook = Folder()



def diary_title_from_date(date: pendulum.DateTime) -> str:
  """Create the title for a diary day based on the datetime
  """
  return f'{date.format("YYYY")}-{date.format("MM")}-{date.format("DD")} {date.format("dddd")} Diary'



def diary_tags_from_date(date: pendulum.DateTime) -> List[str]:
  """Build the list of tags for a diary day
  """
  tags = []
  # .diary tag
  tags.append('.diary')
  # Year. Example: time.2025
  tags.append(f"time.{date.format('YYYY')}")
  # Month. Example: time.february
  tags.append(f"time.{date.format('MMMM').lower()}")
  # Week. Example: time.week_15
  tags.append(f"time.week_{date.strftime('%V')}") 
  # Day. Example: time.day_16
  tags.append(f"time.day_{date.format('DD')}")
  return tags




def diary_text_from_date(date: pendulum.DateTime) -> str:
  """Create a diary note text from a date
  """
  year = date.format('YYYY')
  month_number = date.format('MM')
  month_name = date.format('MMMM').lower()
  day_number = date.format('DD')
  day_name = date.format('dddd')
  query_count_string = '{{count}}'
  list_view_body_string = '"{{body}}"'
  diary_text = f'''# {day_number}-{month_number}-{year} {day_name}
###### tt

<!-- note-overview-plugin
search: tag:.scratchpad -tag:dedimo
fields: body
listview:
  text: "{{body}}"
-->


[⬆️](#tt)
***
<br>



<!-- note-overview-plugin
search: type:note -tag:dedimo -tag:communication* -tag:.event.appointment -tag:event.birthday -tag:media tag:time.{year} tag:time.{month_name} tag:time.day_{day_number}
fields: body
listview:
  text: {list_view_body_string}
-->
<!--endoverview-->

<!-- note-overview-plugin
search: type:note -tag:dedimo tag:time.{year} tag:time.{month_name} tag:time.day_{day_number}
fields: title, image
alias: title AS Notes, image AS Pic
sort: title ASC
details:
  open: true
  summary: Notes - {query_count_string}
-->
<details  open>
<summary>Notes - {query_count_string}</summary>

| Notes |
| --- |
</details>
<!--endoverview-->

<!-- note-overview-plugin
search: type:todo iscompleted:0 -tag:dedimo tag:todo.doing tag:time.{year} tag:time.{month_name} tag:time.day_{day_number}
fields: title
alias: title AS Todo
sort: title ASC
details:
  open: true
  summary: Todo - {query_count_string}
-->
<details  open>
<summary>Todo - {query_count_string}</summary>

| Todo |
| --- |
</details>
<!--endoverview-->

[⬆️](#tt)
***
<br>



| LinkTags |
|-|
| [Diary](:/aa24a870133f4a11996dc85a9e120abb)<br>[2025](:/245e1b37498d4cf9a0baab43862f2422) |
[⬆️](#tt)
***
<br>
  '''
  return diary_text



def create_diary_day(
    date: pendulum.DateTime, 
    notebook: str, 
    api_key: str, 
    settings: Settings, 
    title_creator: Callable[[pendulum.DateTime], str], 
    body_creator: Callable[[pendulum.DateTime], str], 
    tags_creator: Callable[[pendulum.DateTime], List[str]]
) -> str:
    """Create a diary note with all required tags for date
    returns the id for the new note.

    To implement later: Deal with multiple entities coming back from search
    results.
    """
    # Setup the note content, tags and title
    title = title_creator(date)
    body = body_creator(date)
    tags = tags_creator(date)
    # Get the id for the notebook diary note should be saved in
    nb_result = api_notebook.search(api_key, settings, notebook, ['id'])
    parent_id = nb_result['result'][0]['id']
    # Setup data for creating the note
    note_data = {
        'title': title,
        'body': body,
        'parent_id': parent_id
    }
    # Create the note
    created_note = api_note.create(api_key, settings, note_data).json()
    # Add the tags to the note
    for tag in tags:
        # get id for tag
        tag_found = api_tag.search(api_key, settings, query=tag, fields=['id'])
        # Check if tag exists
        if tag_found['result']:
            tag_id = tag_found['result'][0]['id']
        else:
            # Tag doesn't exist, create it.
            created_tag = api_tag.create(
                api_key, settings, {'title': tag}
            ).json()
            tag_id = created_tag['id']
        api_tag.add_to_note(api_key, settings, tag_id, created_note['id'])
    return created_note['id']


def create_diary_month(
    year: int,
    month: int,
    notebook: str, 
    api_key: str, 
    settings: Settings, 
    title_creator: Callable[[pendulum.DateTime], str], 
    body_creator: Callable[[pendulum.DateTime], str], 
    tags_creator: Callable[[pendulum.DateTime], List[str]],
    diary_day_creator: Callable[[
        pendulum.DateTime, 
        str, 
        str, 
        Settings,
        Callable[[pendulum.DateTime], str],
        Callable[[pendulum.DateTime], str],
        Callable[[pendulum.DateTime], List[str]]
    ], str]
) -> List[str]:
    """Create a day diary note for each day in the specified month
    """
    month_days = get_days_in_month(year, month)
    month_note_ids = [] # Store created note id's to be returned to caller
    for day in month_days:
        month_note_ids.append(diary_day_creator(
            day, notebook, api_key, settings, title_creator,
            body_creator, tags_creator
        ))
    return month_note_ids
