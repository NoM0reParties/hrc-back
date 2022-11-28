from typing import List, Tuple, Set, Dict

from models import Feature, FeatureTeamOrder, DeveloperTeam, Developer, DeveloperAssignment
from schemas import FeatureDTO, FeatureTeamOrderDTO, DeveloperDTO, DevTeamDTO


def feature_list_mapper(
        result: List[Tuple[FeatureTeamOrder, Feature, Developer, DeveloperTeam, DeveloperAssignment]]
) -> List[FeatureDTO]:
    results: Dict[int, FeatureDTO] = {}
    for fto, f, d, dt, da in result:
        dt_dto = DevTeamDTO(
            id=dt.id,
            name=dt.name,
        ) if dt is not None else None
        d_dto = DeveloperDTO(
            id=d.id,
            name=f"{d.first_name} {d.last_name}",
            involvement=d.involvement,
            dev_team_id=d.dev_team_id,
        ) if d is not None else None
        fto_dto = FeatureTeamOrderDTO(
            id=fto.id,
            dev_team=dt_dto,
            assigned_developer=d_dto,
            updated=fto.updated,
            assigned=fto.assigned,
            hours=fto.hours,
            auto_assignment=fto.auto_assignment,
            gap=fto.gap,
        ) if fto is not None else None
        if f.id not in results:
            results.setdefault(f.id, FeatureDTO(
                id=f.id, name=f.name, dev_team_orders=[fto_dto] if fto_dto else []
            ))
            continue
        dto: FeatureDTO = results[f.id]
        dto.dev_team_orders.append(fto_dto)
    return list(results.values())
