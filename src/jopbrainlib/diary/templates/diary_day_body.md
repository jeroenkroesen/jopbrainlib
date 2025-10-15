# {{ day_number }}-{{ month_number }}-{{ year }} {{ day_name }}
###### tt

<!-- note-overview-plugin
search: tag:.scratchpad -tag:dedimo
fields: body
listview:
  text: "{% raw %}{{body}}{% endraw %}"
-->


[⬆️](#tt)
***
<br>



<!-- note-overview-plugin
search: type:note -tag:dedimo -tag:no_embed_diary -tag:communication* -tag:.event.appointment -tag:event.birthday -tag:media tag:time.{{ year }} tag:time.{{ month_name }} tag:time.day_{{ day_number }}
fields: body
listview:
  text: "{% raw %}{{body}}{% endraw %}"
-->
<!--endoverview-->

<!-- note-overview-plugin
search: type:note -tag:dedimo tag:time.{{ year }} tag:time.{{ month_name }} tag:time.day_{{ day_number }}
fields: title, image
alias: title AS Notes, image AS Pic
sort: title ASC
details:
  open: true
  summary: Notes - {% raw %}{{count}}{% endraw %}
-->
<details open>
<summary>Notes - </summary>

| Notes |
| --- |
</details>
<!--endoverview-->

<!-- note-overview-plugin
search: type:todo iscompleted:0 -tag:dedimo tag:time.{{ year }} tag:time.{{ month_name }} tag:time.day_{{ day_number }}
fields: title
alias: title AS Todo
sort: title ASC
details:
  open: true
  summary: Todo - {% raw %}{{count}}{% endraw %}
-->
<details open>
<summary>Todo - </summary>

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

