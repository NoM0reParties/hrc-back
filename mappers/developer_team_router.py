from datetime import date, timedelta
from typing import List, Tuple, Set, Dict

from schemas.developer_team import DevTeamBySprintDTO, DeveloperBySprintDTO


def find_possible_working_hours(beginning_date: date, ending_date: date) -> int:
    day = beginning_date
    possible_hours = 0
    while day != ending_date:
        if day.weekday() < 5:
            possible_hours += 8
        day += timedelta(days=1)
    return possible_hours


def dev_team_list_mapper(
        result: List[Tuple[int, int, str, int, int, date, date, int]]
) -> List[DevTeamBySprintDTO]:
    print(result)
    working_hours = 0
    collector: Dict[int, DevTeamBySprintDTO] = {}
    for d_id, d_fn, d_ln, d_inv, dt_id, dt_name, overall_hours, fto_count, sprint_start, sprint_end, team_fto in result:
        if not working_hours:
            working_hours = find_possible_working_hours(sprint_start, sprint_end)
        developer = DeveloperBySprintDTO(
            id=d_id,
            first_name=d_fn,
            last_name=d_ln,
            involvement=d_inv,
            possible_hours=working_hours * d_inv / 100,
            sprint_load=overall_hours or 0,
            fto_count=fto_count,
        ) if d_id else None
        if dt_id not in collector:
            collector.setdefault(dt_id, DevTeamBySprintDTO(
                id=dt_id,
                name=dt_name,
                developers=[developer] if developer else [],
                team_load=overall_hours or 0,
                fto_overall=team_fto or 0,
                fto_assigned=fto_count or 0,
            ))
        else:
            dto = collector[dt_id]
            if developer:
                dto.developers.append(developer)
            dto.fto_assigned += fto_count or 0
            dto.team_load += overall_hours or 0

    return list(collector.values())
