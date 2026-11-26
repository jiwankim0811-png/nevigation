from __future__ import annotations

import heapq
import time
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/algorithm",
    tags=["Algorithm"]
)

# 기본 네비게이션 그래프 (수도권 남부 간선도로 - 강남/양재/판교 축)
DEFAULT_NODES: dict[str, dict[str, Any]] = {
    "A": {"name": "강남역", "role": "출발 거점", "x": 120, "y": 180},
    "B": {"name": "양재역", "role": "주요 환승지", "x": 290, "y": 120},
    "C": {"name": "우면산로", "role": "우회 간선", "x": 260, "y": 290},
    "D": {"name": "양재시민숲", "role": "경부선 분기점", "x": 480, "y": 230},
    "F": {"name": "청계산입구", "role": "외곽 간선", "x": 520, "y": 110},
    "H": {"name": "대왕판교", "role": "판교 진입로", "x": 440, "y": 350},
    "E": {"name": "판교역", "role": "중심 역사", "x": 780, "y": 150},
    "J": {"name": "정자역", "role": "분당선 분기점", "x": 740, "y": 310},
    "G": {"name": "테크노밸리", "role": "최종 목적지", "x": 1050, "y": 210},
}

DEFAULT_EDGES: list[dict[str, Any]] = [
    {"from": "A", "to": "B", "dist": 3.2, "time": 5.0, "road": "강남대로"},
    {"from": "A", "to": "C", "dist": 4.8, "time": 8.0, "road": "우면산로"},
    {"from": "B", "to": "F", "dist": 6.5, "time": 10.0, "road": "청계산로"},
    {"from": "B", "to": "D", "dist": 2.1, "time": 3.0, "road": "매헌로"},
    {"from": "C", "to": "D", "dist": 3.0, "time": 5.0, "road": "양재대로"},
    {"from": "C", "to": "H", "dist": 5.2, "time": 7.0, "road": "대왕판교로"},
    {"from": "F", "to": "E", "dist": 5.5, "time": 9.0, "road": "신분당선"},
    {"from": "D", "to": "E", "dist": 4.0, "time": 6.0, "road": "경부간선"},
    {"from": "D", "to": "J", "dist": 6.0, "time": 8.0, "road": "분당내곡간"},
    {"from": "H", "to": "J", "dist": 4.5, "time": 6.0, "road": "판교원로"},
    {"from": "E", "to": "G", "dist": 3.4, "time": 5.0, "road": "테크노중앙로"},
    {"from": "J", "to": "G", "dist": 4.2, "time": 7.0, "road": "대왕판교로"},
    {"from": "E", "to": "J", "dist": 3.0, "time": 4.0, "road": "성남대로"},
]


class StandardResponse(BaseModel):
    success: bool
    data: Any | None = None
    message: str | None = None


class DijkstraRequest(BaseModel):
    start_node: str = Field(default="A", description="출발 노드 ID (기본값: A)")
    end_node: str = Field(default="G", description="도착 노드 ID (기본값: G)")
    metric: str = Field(default="dist", description="가중치 기준: 'dist' (거리 km) 또는 'time' (소요시간 분)")
    custom_nodes: Optional[dict[str, dict[str, Any]]] = Field(default=None, description="커스텀 노드 목록")
    custom_edges: Optional[list[dict[str, Any]]] = Field(default=None, description="커스텀 간선 목록")


def build_histogram(distances: dict[str, float], settled: set[str], current: Optional[str], nodes_meta: dict[str, dict[str, Any]], unit: str) -> dict[str, Any]:
    """각 단계별 노드 거리 히스토그램 및 노드별 최단거리 바 데이터 생성"""
    step_size = 3.0 if unit == "km" else 4.0
    bins = [
        {"range": f"0~{step_size:g}{unit}", "min": 0.0, "max": step_size, "count": 0, "nodes": []},
        {"range": f"{step_size:g}~{step_size*2:g}{unit}", "min": step_size, "max": step_size * 2, "count": 0, "nodes": []},
        {"range": f"{step_size*2:g}~{step_size*3:g}{unit}", "min": step_size * 2, "max": step_size * 3, "count": 0, "nodes": []},
        {"range": f"{step_size*3:g}~{step_size*4:g}{unit}", "min": step_size * 3, "max": step_size * 4, "count": 0, "nodes": []},
        {"range": f"{step_size*4:g}{unit}+", "min": step_size * 4, "max": float("inf"), "count": 0, "nodes": []},
        {"range": "미도달(∞)", "min": -1.0, "max": -1.0, "count": 0, "nodes": []},
    ]

    node_bars = []
    for nid, meta in nodes_meta.items():
        d = distances.get(nid, float("inf"))
        
        if nid == current:
            node_status = "evaluating"
        elif nid in settled:
            node_status = "settled"
        elif d < float("inf"):
            node_status = "queued"
        else:
            node_status = "unvisited"

        node_bars.append({
            "id": nid,
            "name": meta.get("name", nid),
            "distance": round(d, 2) if d < float("inf") else None,
            "status": node_status
        })

        if d == float("inf"):
            bins[-1]["count"] += 1
            bins[-1]["nodes"].append(nid)
        else:
            placed = False
            for b in bins[:-1]:
                if b["min"] <= d < b["max"]:
                    b["count"] += 1
                    b["nodes"].append(nid)
                    placed = True
                    break
            if not placed and d >= step_size * 4:
                bins[-2]["count"] += 1
                bins[-2]["nodes"].append(nid)

    return {
        "bins": bins,
        "node_bars": node_bars,
        "finite_count": sum(1 for d in distances.values() if d < float("inf")),
        "infinite_count": sum(1 for d in distances.values() if d == float("inf")),
    }


@router.post("/dijkstra", response_model=StandardResponse, status_code=status.HTTP_200_OK)
async def run_dijkstra_simulation(payload: DijkstraRequest) -> StandardResponse:
    """
    다익스트라 알고리즘을 실행하고 단계별 스냅샷, 히스토그램, 메타데이터(시간복잡도, 지연시간)를 반환합니다.
    """
    try:
        t_start_total = time.perf_counter()

        nodes = payload.custom_nodes or DEFAULT_NODES
        edges = payload.custom_edges or DEFAULT_EDGES
        start_node = payload.start_node
        end_node = payload.end_node
        metric_key = "dist" if payload.metric == "dist" else "time"
        unit = "km" if metric_key == "dist" else "분"

        if start_node not in nodes:
            raise HTTPException(status_code=400, detail=f"출발 노드 '{start_node}'가 그래프에 존재하지 않습니다.")
        if end_node not in nodes:
            raise HTTPException(status_code=400, detail=f"도착 노드 '{end_node}'가 그래프에 존재하지 않습니다.")

        adj: dict[str, list[dict[str, Any]]] = {nid: [] for nid in nodes}
        for edge in edges:
            u, v = edge["from"], edge["to"]
            w = float(edge.get(metric_key, edge.get("dist", 1.0)))
            road = edge.get("road", "일반도로")
            if u in adj and v in adj:
                adj[u].append({"to": v, "weight": w, "road": road})
                adj[v].append({"to": u, "weight": w, "road": road})

        distances: dict[str, float] = {nid: float("inf") for nid in nodes}
        distances[start_node] = 0.0
        predecessors: dict[str, Optional[str]] = {nid: None for nid in nodes}
        settled_nodes: set[str] = set()

        pq: list[tuple[float, str]] = []
        heapq.heappush(pq, (0.0, start_node))

        steps: list[dict[str, Any]] = []
        step_number = 0
        total_ops = 0
        accumulated_us = 0.0

        t0 = time.perf_counter()
        hist0 = build_histogram(distances, settled_nodes, None, nodes, unit)
        step_us = (time.perf_counter() - t0) * 1_000_000
        accumulated_us += step_us
        total_ops += len(nodes)

        steps.append({
            "step": step_number,
            "phase": "INIT",
            "current_node": None,
            "neighbor_node": None,
            "distances": {k: (round(v, 2) if v < float("inf") else "inf") for k, v in distances.items()},
            "predecessors": dict(predecessors),
            "settled": list(settled_nodes),
            "queue": [{"node": start_node, "dist": 0.0, "prev": None}],
            "relaxed_edge": None,
            "histogram": hist0,
            "step_duration_us": round(step_us, 2),
            "accumulated_duration_us": round(accumulated_us, 2),
            "complexity_metric": {
                "step_operation": "Initialize: O(V)",
                "theoretical_formula": "O((V + E) log V)",
                "total_ops_so_far": total_ops,
                "explored_nodes": 0,
                "relaxed_edges_count": 0
            },
            "pseudocode_line": "d[v] = ∞ for all v; d[start] = 0; Q.insert(start, 0)",
            "log_message": f"탐색 시작: {nodes[start_node]['name']}({start_node}) 초기 거리 0으로 큐 삽입."
        })

        relaxed_count = 0
        target_reached = False

        while pq:
            step_t_start = time.perf_counter()
            curr_dist, u = heapq.heappop(pq)
            total_ops += 1

            if u in settled_nodes:
                continue

            step_number += 1
            hist_extract = build_histogram(distances, settled_nodes, u, nodes, unit)
            step_us = (time.perf_counter() - step_t_start) * 1_000_000
            accumulated_us += step_us

            steps.append({
                "step": step_number,
                "phase": "EXTRACT_MIN",
                "current_node": u,
                "neighbor_node": None,
                "distances": {k: (round(v, 2) if v < float("inf") else "inf") for k, v in distances.items()},
                "predecessors": dict(predecessors),
                "settled": list(settled_nodes),
                "queue": [{"node": item[1], "dist": round(item[0], 2), "prev": predecessors[item[1]]} for item in sorted(pq)],
                "relaxed_edge": None,
                "histogram": hist_extract,
                "step_duration_us": round(step_us, 2),
                "accumulated_duration_us": round(accumulated_us, 2),
                "complexity_metric": {
                    "step_operation": "ExtractMin: O(log V)",
                    "theoretical_formula": "O((V + E) log V)",
                    "total_ops_so_far": total_ops,
                    "explored_nodes": len(settled_nodes) + 1,
                    "relaxed_edges_count": relaxed_count
                },
                "pseudocode_line": f"u = ExtractMin(Q) → {u} (최소 추정거리: {curr_dist}{unit})",
                "log_message": f"최소 힙에서 노드 {nodes[u]['name']}({u}) 추출 (거리: {curr_dist}{unit})."
            })

            if u == end_node:
                settled_nodes.add(u)
                target_reached = True
                break

            for edge in adj[u]:
                v = edge["to"]
                weight = edge["weight"]
                road_name = edge["road"]

                if v in settled_nodes:
                    continue

                total_ops += 1
                step_t_relax = time.perf_counter()
                old_dist = distances[v]
                new_dist = curr_dist + weight

                is_relaxed = new_dist < old_dist
                if is_relaxed:
                    distances[v] = new_dist
                    predecessors[v] = u
                    heapq.heappush(pq, (new_dist, v))
                    total_ops += 1
                    relaxed_count += 1

                step_number += 1
                hist_relax = build_histogram(distances, settled_nodes, u, nodes, unit)
                step_us = (time.perf_counter() - step_t_relax) * 1_000_000
                accumulated_us += step_us

                old_str = f"{old_dist:.1f}" if old_dist < float("inf") else "∞"
                new_str = f"{new_dist:.1f}"

                steps.append({
                    "step": step_number,
                    "phase": "RELAX_SUCCESS" if is_relaxed else "RELAX_SKIP",
                    "current_node": u,
                    "neighbor_node": v,
                    "distances": {k: (round(val, 2) if val < float("inf") else "inf") for k, val in distances.items()},
                    "predecessors": dict(predecessors),
                    "settled": list(settled_nodes),
                    "queue": [{"node": item[1], "dist": round(item[0], 2), "prev": predecessors[item[1]]} for item in sorted(pq)],
                    "relaxed_edge": {
                        "from": u,
                        "to": v,
                        "weight": weight,
                        "road": road_name,
                        "old_dist": old_str,
                        "new_dist": new_str,
                        "is_relaxed": is_relaxed
                    },
                    "histogram": hist_relax,
                    "step_duration_us": round(step_us, 2),
                    "accumulated_duration_us": round(accumulated_us, 2),
                    "complexity_metric": {
                        "step_operation": f"Relaxation: d[{v}] = min({old_str}, {curr_dist:.1f} + {weight:.1f})",
                        "theoretical_formula": "O((V + E) log V)",
                        "total_ops_so_far": total_ops,
                        "explored_nodes": len(settled_nodes) + 1,
                        "relaxed_edges_count": relaxed_count
                    },
                    "pseudocode_line": (
                        f"if d[{u}] + w({u},{v}) < d[{v}]: d[{v}] ← {new_str} (이완 성공)"
                        if is_relaxed else
                        f"d[{u}] + w({u},{v}) >= d[{v}] (기존 경로 유지: {old_str})"
                    ),
                    "log_message": (
                        f"간선 이완: {nodes[u]['name']}→{nodes[v]['name']} ({road_name}, 가중치 {weight}{unit}), 거리 갱신: {old_str} → {new_str}{unit}."
                        if is_relaxed else
                        f"간선 검사: {nodes[u]['name']}→{nodes[v]['name']} (기존 최단거리 {old_str}{unit}가 더 우수하여 유지)."
                    )
                })

            settled_nodes.add(u)

        path = []
        curr = end_node
        if distances[end_node] < float("inf"):
            while curr is not None:
                path.append(curr)
                curr = predecessors[curr]
            path.reverse()

        t_complete = time.perf_counter()
        final_hist = build_histogram(distances, settled_nodes, None, nodes, unit)
        final_step_us = (time.perf_counter() - t_complete) * 1_000_000
        accumulated_us += final_step_us

        step_number += 1
        steps.append({
            "step": step_number,
            "phase": "COMPLETE",
            "current_node": None,
            "neighbor_node": None,
            "distances": {k: (round(val, 2) if val < float("inf") else "inf") for k, val in distances.items()},
            "predecessors": dict(predecessors),
            "settled": list(settled_nodes),
            "queue": [],
            "relaxed_edge": None,
            "histogram": final_hist,
            "step_duration_us": round(final_step_us, 2),
            "accumulated_duration_us": round(accumulated_us, 2),
            "complexity_metric": {
                "step_operation": "Done: Optimal Path Backtracking",
                "theoretical_formula": "O((V + E) log V)",
                "total_ops_so_far": total_ops,
                "explored_nodes": len(settled_nodes),
                "relaxed_edges_count": relaxed_count
            },
            "pseudocode_line": f"return ShortestPath(start={start_node}, end={end_node})",
            "log_message": f"최적 경로 탐색 완료! 최단 {unit}: {distances[end_node]:.1f}{unit}, 경유: {' → '.join(path)}."
        })

        total_exec_ms = (time.perf_counter() - t_start_total) * 1000

        result_data = {
            "start_node": start_node,
            "end_node": end_node,
            "metric": metric_key,
            "unit": unit,
            "target_reached": target_reached,
            "shortest_path": path,
            "shortest_distance": round(distances[end_node], 2) if distances[end_node] < float("inf") else None,
            "total_steps": len(steps),
            "total_relaxed_count": relaxed_count,
            "total_execution_time_ms": round(total_exec_ms, 4),
            "total_accumulated_us": round(accumulated_us, 2),
            "graph": {
                "nodes": nodes,
                "edges": edges
            },
            "steps": steps
        }

        return StandardResponse(
            success=True,
            data=result_data,
            message="다익스트라 알고리즘 시뮬레이션 데이터가 성공적으로 생성되었습니다."
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"다익스트라 알고리즘 수행 중 오류 발생: {str(e)}"
        )


@router.get("/health", response_model=StandardResponse)
async def health_check() -> StandardResponse:
    return StandardResponse(
        success=True,
        data={"status": "healthy", "service": "dijkstra_navigation_engine"},
        message="Algorithm router is operational."
    )
