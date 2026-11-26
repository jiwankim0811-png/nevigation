/**
 * Google Apps Script Backend for Dijkstra Navigation Graph Visualizer
 */

function doGet(e) {
  if (e && e.parameter && e.parameter.setServiceUrl) {
    PropertiesService.getScriptProperties().setProperty('BACKEND_SERVICE_URL', e.parameter.setServiceUrl);
    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'Backend URL updated in script properties: ' + e.parameter.setServiceUrl
    })).setMimeType(ContentService.MimeType.JSON);
  }

  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('다익스트라 알고리즘 길찾기 시각화 시뮬레이터 (GraphFlow v2.4 Core)')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function doPost(e) {
  try {
    const contents = e.postData.contents;
    const data = JSON.parse(contents);

    // Cloud Run / FastAPI 백엔드 URL 등록 웹훅
    if (data.serviceUrl) {
      PropertiesService.getScriptProperties().setProperty('BACKEND_SERVICE_URL', data.serviceUrl);
      return ContentService.createTextOutput(JSON.stringify({
        status: 'success',
        message: 'Backend URL updated successfully: ' + data.serviceUrl
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // 시뮬레이션 데이터 요청 프록시
    if (data.action === 'simulate') {
      const result = getSimulationData(data.payload || {});
      return ContentService.createTextOutput(JSON.stringify({
        status: 'success',
        data: result
      })).setMimeType(ContentService.MimeType.JSON);
    }

    return ContentService.createTextOutput(JSON.stringify({
      status: 'ok',
      received: data
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * 프론트엔드에서 google.script.run.getSimulationData(...) 로 직접 호출 가능한 함수
 */
function getSimulationData(payload) {
  let backendUrl = PropertiesService.getScriptProperties().getProperty('BACKEND_SERVICE_URL');
  if (!backendUrl) {
    backendUrl = 'https://nevigation-server-epaw6mtefq-uc.a.run.app';
  }

  // 1. 외부 FastAPI 백엔드가 등록되어 있다면 호출 시도
  if (backendUrl) {
    try {
      const endpoint = backendUrl.replace(/\/+$/, '') + '/api/algorithm/dijkstra';
      const options = {
        method: 'post',
        contentType: 'application/json',
        payload: JSON.stringify(payload || { start_node: 'A', end_node: 'G', metric: 'dist' }),
        muteHttpExceptions: true
      };
      const response = UrlFetchApp.fetch(endpoint, options);
      if (response.getResponseCode() === 200) {
        const json = JSON.parse(response.getContentText());
        if (json.success && json.data) {
          json.data.source = 'fastapi_backend';
          return json.data;
        }
      }
    } catch (e) {
      Logger.log('FastAPI backend fetch failed, using fallback engine: ' + e);
    }
  }

  // 2. 내장 다익스트라 엔진 (Standalone Fallback Engine)
  return runBuiltinDijkstra(payload);
}

/**
 * GAS 내장 다익스트라 알고리즘 & 단계별 히스토그램/메타데이터 생성기
 */
function runBuiltinDijkstra(payload) {
  const startNode = (payload && payload.start_node) || 'A';
  const endNode = (payload && payload.end_node) || 'G';
  const metric = (payload && payload.metric === 'time') ? 'time' : 'dist';
  const unit = metric === 'dist' ? 'km' : '분';

  const NODES = {
    "A": { name: "강남역", role: "출발 거점", x: 120, y: 180 },
    "B": { name: "양재역", role: "주요 환승지", x: 290, y: 120 },
    "C": { name: "우면산로", role: "우회 간선", x: 260, y: 290 },
    "D": { name: "양재시민숲", role: "경부선 분기점", x: 480, y: 230 },
    "F": { name: "청계산입구", role: "외곽 간선", x: 520, y: 110 },
    "H": { name: "대왕판교", role: "판교 진입로", x: 440, y: 350 },
    "E": { name: "판교역", role: "중심 역사", x: 780, y: 150 },
    "J": { name: "정자역", role: "분당선 분기점", x: 740, y: 310 },
    "G": { name: "테크노밸리", role: "최종 목적지", x: 1050, y: 210 }
  };

  const EDGES = [
    { from: "A", to: "B", dist: 3.2, time: 5.0, road: "강남대로" },
    { from: "A", to: "C", dist: 4.8, time: 8.0, road: "우면산로" },
    { from: "B", to: "F", dist: 6.5, time: 10.0, road: "청계산로" },
    { from: "B", to: "D", dist: 2.1, time: 3.0, road: "매헌로" },
    { from: "C", to: "D", dist: 3.0, time: 5.0, road: "양재대로" },
    { from: "C", to: "H", dist: 5.2, time: 7.0, road: "대왕판교로" },
    { from: "F", to: "E", dist: 5.5, time: 9.0, road: "신분당선" },
    { from: "D", to: "E", dist: 4.0, time: 6.0, road: "경부간선" },
    { from: "D", to: "J", dist: 6.0, time: 8.0, road: "분당내곡간" },
    { from: "H", to: "J", dist: 4.5, time: 6.0, road: "판교원로" },
    { from: "E", to: "G", dist: 3.4, time: 5.0, road: "테크노중앙로" },
    { from: "J", to: "G", dist: 4.2, time: 7.0, road: "대왕판교로" },
    { from: "E", to: "J", dist: 3.0, time: 4.0, road: "성남대로" }
  ];

  const adj = {};
  for (let nid in NODES) adj[nid] = [];
  for (let e of EDGES) {
    const w = metric === 'dist' ? e.dist : e.time;
    adj[e.from].push({ to: e.to, weight: w, road: e.road });
    adj[e.to].push({ to: e.from, weight: w, road: e.road });
  }

  const distances = {};
  const predecessors = {};
  const settled = {};
  for (let nid in NODES) {
    distances[nid] = Infinity;
    predecessors[nid] = null;
    settled[nid] = false;
  }
  distances[startNode] = 0.0;

  // 우선순위 큐 배열
  let pq = [{ node: startNode, dist: 0.0 }];
  const steps = [];
  let stepNum = 0;
  let relaxedCount = 0;
  let totalOps = Object.keys(NODES).length;
  let accumUs = 25.0;

  function makeHistogram(currNode) {
    const stepSize = metric === 'dist' ? 3.0 : 4.0;
    const bins = [
      { range: "0~" + stepSize + unit, min: 0.0, max: stepSize, count: 0, nodes: [] },
      { range: stepSize + "~" + (stepSize * 2) + unit, min: stepSize, max: stepSize * 2, count: 0, nodes: [] },
      { range: (stepSize * 2) + "~" + (stepSize * 3) + unit, min: stepSize * 2, max: stepSize * 3, count: 0, nodes: [] },
      { range: (stepSize * 3) + "~" + (stepSize * 4) + unit, min: stepSize * 3, max: stepSize * 4, count: 0, nodes: [] },
      { range: (stepSize * 4) + unit + "+", min: stepSize * 4, max: Infinity, count: 0, nodes: [] },
      { range: "미도달(∞)", min: -1.0, max: -1.0, count: 0, nodes: [] }
    ];

    const nodeBars = [];
    for (let nid in NODES) {
      const d = distances[nid];
      let status = 'unvisited';
      if (nid === currNode) status = 'evaluating';
      else if (settled[nid]) status = 'settled';
      else if (d < Infinity) status = 'queued';

      nodeBars.push({
        id: nid,
        name: NODES[nid].name,
        distance: d < Infinity ? Math.round(d * 100) / 100 : null,
        status: status
      });

      if (d === Infinity) {
        bins[bins.length - 1].count++;
        bins[bins.length - 1].nodes.push(nid);
      } else {
        let placed = false;
        for (let i = 0; i < bins.length - 1; i++) {
          if (d >= bins[i].min && d < bins[i].max) {
            bins[i].count++;
            bins[i].nodes.push(nid);
            placed = true;
            break;
          }
        }
        if (!placed) {
          bins[4].count++;
          bins[4].nodes.push(nid);
        }
      }
    }

    return { bins: bins, node_bars: nodeBars };
  }

  // Step 0: 초기화
  steps.push({
    step: 0,
    phase: "INIT",
    current_node: null,
    neighbor_node: null,
    distances: Object.assign({}, distances),
    predecessors: Object.assign({}, predecessors),
    settled: [],
    queue: pq.slice(),
    relaxed_edge: null,
    histogram: makeHistogram(null),
    step_duration_us: 18.5,
    accumulated_duration_us: accumUs,
    complexity_metric: {
      step_operation: "Initialize: O(V)",
      theoretical_formula: "O((V + E) log V)",
      total_ops_so_far: totalOps,
      explored_nodes: 0,
      relaxed_edges_count: 0
    },
    pseudocode_line: "d[v] = ∞ for all v; d[start] = 0; Q.insert(start, 0)",
    log_message: "탐색 초기화: " + NODES[startNode].name + "(" + startNode + ") 거리 0으로 큐 삽입."
  });

  while (pq.length > 0) {
    pq.sort(function(a, b) { return a.dist - b.dist; });
    const top = pq.shift();
    const u = top.node;
    const currDist = top.dist;
    totalOps++;

    if (settled[u]) continue;

    stepNum++;
    accumUs += 12.0;

    const settledList = Object.keys(settled).filter(function(k) { return settled[k]; });

    steps.push({
      step: stepNum,
      phase: "EXTRACT_MIN",
      current_node: u,
      neighbor_node: null,
      distances: Object.assign({}, distances),
      predecessors: Object.assign({}, predecessors),
      settled: settledList.slice(),
      queue: pq.map(function(item) {
        return { node: item.node, dist: Math.round(item.dist * 10) / 10, prev: predecessors[item.node] };
      }),
      relaxed_edge: null,
      histogram: makeHistogram(u),
      step_duration_us: 14.2,
      accumulated_duration_us: accumUs,
      complexity_metric: {
        step_operation: "ExtractMin: O(log V)",
        theoretical_formula: "O((V + E) log V)",
        total_ops_so_far: totalOps,
        explored_nodes: settledList.length + 1,
        relaxed_edges_count: relaxedCount
      },
      pseudocode_line: "u = ExtractMin(Q) → " + u + " (" + currDist + unit + ")",
      log_message: "최소 힙에서 " + NODES[u].name + "(" + u + ") 추출 (확정거리: " + currDist + unit + ")."
    });

    if (u === endNode) {
      settled[u] = true;
      break;
    }

    const neighbors = adj[u] || [];
    for (let i = 0; i < neighbors.length; i++) {
      const edge = neighbors[i];
      const v = edge.to;
      const weight = edge.weight;
      if (settled[v]) continue;

      totalOps++;
      const oldDist = distances[v];
      const newDist = currDist + weight;
      const isRelaxed = newDist < oldDist;

      if (isRelaxed) {
        distances[v] = newDist;
        predecessors[v] = u;
        pq.push({ node: v, dist: newDist });
        relaxedCount++;
        totalOps++;
      }

      stepNum++;
      accumUs += 15.4;

      const oldStr = oldDist < Infinity ? (Math.round(oldDist * 10) / 10) : "∞";
      const newStr = Math.round(newDist * 10) / 10;

      steps.push({
        step: stepNum,
        phase: isRelaxed ? "RELAX_SUCCESS" : "RELAX_SKIP",
        current_node: u,
        neighbor_node: v,
        distances: Object.assign({}, distances),
        predecessors: Object.assign({}, predecessors),
        settled: Object.keys(settled).filter(function(k) { return settled[k]; }),
        queue: pq.map(function(item) {
          return { node: item.node, dist: Math.round(item.dist * 10) / 10, prev: predecessors[item.node] };
        }),
        relaxed_edge: {
          from: u,
          to: v,
          weight: weight,
          road: edge.road,
          old_dist: oldStr,
          new_dist: newStr,
          is_relaxed: isRelaxed
        },
        histogram: makeHistogram(u),
        step_duration_us: 16.0,
        accumulated_duration_us: accumUs,
        complexity_metric: {
          step_operation: "Relaxation: d[" + v + "] = min(" + oldStr + ", " + currDist + " + " + weight + ")",
          theoretical_formula: "O((V + E) log V)",
          total_ops_so_far: totalOps,
          explored_nodes: Object.keys(settled).filter(function(k) { return settled[k]; }).length + 1,
          relaxed_edges_count: relaxedCount
        },
        pseudocode_line: isRelaxed ?
          "if d[" + u + "] + w(" + u + "," + v + ") < d[" + v + "]: d[" + v + "] ← " + newStr + " (이완 성공)" :
          "d[" + u + "] + w(" + u + "," + v + ") >= d[" + v + "] (기존 경로 유지: " + oldStr + ")",
        log_message: isRelaxed ?
          "간선 이완: " + NODES[u].name + "→" + NODES[v].name + " (" + edge.road + "), 거리 갱신: " + oldStr + " → " + newStr + unit + "." :
          "간선 검사: " + NODES[u].name + "→" + NODES[v].name + " (기존 최단거리 " + oldStr + unit + " 유지)."
      });
    }

    settled[u] = true;
  }

  // 최단 경로 역추적
  const path = [];
  let curr = endNode;
  if (distances[endNode] < Infinity) {
    while (curr) {
      path.push(curr);
      curr = predecessors[curr];
    }
    path.reverse();
  }

  stepNum++;
  accumUs += 10.0;
  steps.push({
    step: stepNum,
    phase: "COMPLETE",
    current_node: null,
    neighbor_node: null,
    distances: Object.assign({}, distances),
    predecessors: Object.assign({}, predecessors),
    settled: Object.keys(settled).filter(function(k) { return settled[k]; }),
    queue: [],
    relaxed_edge: null,
    histogram: makeHistogram(null),
    step_duration_us: 10.0,
    accumulated_duration_us: accumUs,
    complexity_metric: {
      step_operation: "Done: Optimal Path Backtracking",
      theoretical_formula: "O((V + E) log V)",
      total_ops_so_far: totalOps,
      explored_nodes: Object.keys(settled).filter(function(k) { return settled[k]; }).length,
      relaxed_edges_count: relaxedCount
    },
    pseudocode_line: "return ShortestPath(start=" + startNode + ", end=" + endNode + ")",
    log_message: "최적 경로 탐색 완료! 최단 " + unit + ": " + (Math.round(distances[endNode] * 10) / 10) + unit + ", 경로: " + path.join(" → ")
  });

  return {
    start_node: startNode,
    end_node: endNode,
    metric: metric,
    unit: unit,
    target_reached: distances[endNode] < Infinity,
    shortest_path: path,
    shortest_distance: Math.round(distances[endNode] * 10) / 10,
    total_steps: steps.length,
    total_relaxed_count: relaxedCount,
    total_execution_time_ms: Math.round(accumUs / 10) / 100,
    total_accumulated_us: Math.round(accumUs * 10) / 10,
    graph: { nodes: NODES, edges: EDGES },
    steps: steps,
    source: 'gas_builtin'
  };
}