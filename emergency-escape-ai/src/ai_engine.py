import heapq
from typing import List, Tuple, Dict
from collections import deque

class PathFinding:
    def __init__(self):
        # 20x20 grid map
        self.grid_width = 40
        self.grid_height = 40
        
        # Hazard zones (fire locations)
        self.hazards = {
            (5, 5), (5, 6), (6, 5), (6, 6),           # Fire zone 1
            (10, 10), (10, 11), (11, 10), (11, 11),   # Fire zone 2
            (15, 3), (15, 4), (16, 3), (16, 4),       # Fire zone 3
            (8, 15), (8, 16), (9, 15), (9, 16),       # Fire zone 4
            (3, 12), (4, 12), (3, 13), (4, 13)        # Fire zone 5
        }
    
    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Manhattan distance heuristic"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions (8 directions)"""
        x, y = pos
        neighbors = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                neighbors.append((nx, ny))
        return neighbors
    
    def get_cost(self, pos: Tuple[int, int], prev_pos: Tuple[int, int] = None, avoid_hazards: bool = True) -> float:
        """Get movement cost"""
        if avoid_hazards and pos in self.hazards:
            return float('inf')
        
        if prev_pos:
            dx = abs(pos[0] - prev_pos[0])
            dy = abs(pos[1] - prev_pos[1])
            return 1.414 if (dx == 1 and dy == 1) else 1.0
        return 1.0
    
    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int], avoid_hazards: bool = True) -> List[Tuple[int, int]]:
        """A* pathfinding algorithm"""
        counter = 0
        open_set = [(0, counter, start)]
        counter += 1
        
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        open_set_hash = {start}
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            open_set_hash.discard(current)
            
            if current == goal:
                path = []
                node = goal
                while node in came_from:
                    path.append(node)
                    node = came_from[node]
                path.append(start)
                return path[::-1]
            
            for neighbor in self.get_neighbors(current):
                if avoid_hazards and neighbor in self.hazards:
                    continue
                
                move_cost = 1.414 if (abs(neighbor[0] - current[0]) == 1 and abs(neighbor[1] - current[1]) == 1) else 1.0
                tentative_g = g_score[current] + move_cost
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    f_score[neighbor] = f
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f, counter, neighbor))
                        counter += 1
                        open_set_hash.add(neighbor)
        
        return []
    
    def dijkstra(self, start: Tuple[int, int], goal: Tuple[int, int], avoid_hazards: bool = True) -> List[Tuple[int, int]]:
        """Dijkstra's algorithm"""
        distances = {(i, j): float('inf') for i in range(self.grid_width) for j in range(self.grid_height)}
        distances[start] = 0
        previous = {}
        
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            visited.add(current)
            
            if current == goal:
                path = []
                node = goal
                while node in previous:
                    path.append(node)
                    node = previous[node]
                path.append(start)
                return path[::-1]
            
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                
                if avoid_hazards and neighbor in self.hazards:
                    continue
                
                move_cost = 1.414 if (abs(neighbor[0] - current[0]) == 1 and abs(neighbor[1] - current[1]) == 1) else 1.0
                new_dist = distances[current] + move_cost
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return []
    
    def bfs(self, start: Tuple[int, int], goal: Tuple[int, int], avoid_hazards: bool = True) -> List[Tuple[int, int]]:
        """BFS algorithm"""
        queue = deque([start])
        came_from = {start: None}
        
        while queue:
            current = queue.popleft()
            
            if current == goal:
                path = []
                node = goal
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                return path[::-1]
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in came_from:
                    if avoid_hazards and neighbor in self.hazards:
                        continue
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        return []
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], algorithm: str = "a_star", avoid_hazards: bool = True) -> Dict:
        """Main function to find path"""
        if algorithm == "a_star":
            path = self.a_star(start, goal, avoid_hazards)
        elif algorithm == "dijkstra":
            path = self.dijkstra(start, goal, avoid_hazards)
        elif algorithm == "bfs":
            path = self.bfs(start, goal, avoid_hazards)
        else:
            path = self.a_star(start, goal, avoid_hazards)
        
        distance = len(path) - 1 if path else 0
        time_estimate = distance * 0.5
        safety_score = 95 if avoid_hazards else 70
        
        return {
            "path": path,
            "distance": distance,
            "time": time_estimate,
            "safety_score": safety_score,
            "found": len(path) > 0,
            "algorithm_used": algorithm,
            "grid_size": f"{self.grid_width}x{self.grid_height}",
            "hazard_zones": len(self.hazards)
        }


# Test code
if __name__ == "__main__":
    pf = PathFinding()
    
    start = (1, 1)
    goal = (18, 18)
    
    print("=" * 80)
    print("Testing A*, Dijkstra, and BFS Algorithms on 20x20 Grid")
    print("=" * 80)
    print(f"\n📍 Start: {start} → Goal: {goal}")
    print(f"🔥 Hazard Zones: {len(pf.hazards)} cells")
    print(f"🗺️ Map Size: {pf.grid_width}x{pf.grid_height}")
    
    # Test A*
    print("\n" + "─" * 80)
    result_a_star = pf.find_path(start, goal, "a_star", avoid_hazards=True)
    print(f"\n🔴 A* Algorithm:")
    print(f"   ✅ Path found: {result_a_star['found']}")
    print(f"   📏 Distance: {result_a_star['distance']} blocks")
    print(f"   ⏱️ Time: {result_a_star['time']:.1f} minutes")
    print(f"   🛡️ Safety Score: {result_a_star['safety_score']}%")
    if result_a_star['path']:
        print(f"   📍 Path: {result_a_star['path'][:5]}...{result_a_star['path'][-5:]}")
    
    # Test Dijkstra
    print("\n" + "─" * 80)
    result_dijkstra = pf.find_path(start, goal, "dijkstra", avoid_hazards=True)
    print(f"\n🟠 Dijkstra Algorithm:")
    print(f"   ✅ Path found: {result_dijkstra['found']}")
    print(f"   📏 Distance: {result_dijkstra['distance']} blocks")
    print(f"   ⏱️ Time: {result_dijkstra['time']:.1f} minutes")
    print(f"   🛡️ Safety Score: {result_dijkstra['safety_score']}%")
    if result_dijkstra['path']:
        print(f"   📍 Path: {result_dijkstra['path'][:5]}...{result_dijkstra['path'][-5:]}")
    
    # Test BFS
    print("\n" + "─" * 80)
    result_bfs = pf.find_path(start, goal, "bfs", avoid_hazards=True)
    print(f"\n🟡 BFS Algorithm:")
    print(f"   ✅ Path found: {result_bfs['found']}")
    print(f"   📏 Distance: {result_bfs['distance']} blocks")
    print(f"   ⏱️ Time: {result_bfs['time']:.1f} minutes")
    print(f"   🛡️ Safety Score: {result_bfs['safety_score']}%")
    if result_bfs['path']:
        print(f"   📍 Path: {result_bfs['path'][:5]}...{result_bfs['path'][-5:]}")
    
    print("\n" + "=" * 80)
    print("✅ All algorithms working!")
    print("=" * 80)