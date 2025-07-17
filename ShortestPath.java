import java.util.*;

class GeoPosition {
    public final double lat;
    public final double lon;
    public GeoPosition(double lat, double lon) {
        this.lat = lat;
        this.lon = lon;
    }
}

class Node {
    public final String id;
    public final GeoPosition pos;
    public Node(String id, GeoPosition pos) {
        this.id = id;
        this.pos = pos;
    }
}

class Edge {
    public final Node from;
    public final Node to;
    public final double weight; // distance in km
    public Edge(Node from, Node to) {
        this.from = from;
        this.to = to;
        this.weight = GeoUtils.haversine(from.pos, to.pos);
    }
}

class GeoUtils {
    private static final double R = 6371.0; // Earth radius in km
    static double haversine(GeoPosition a, GeoPosition b) {
        return haversine(a.lat, a.lon, b.lat, b.lon);
    }
    static double haversine(double lat1, double lon1, double lat2, double lon2) {
        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);
        double rLat1 = Math.toRadians(lat1);
        double rLat2 = Math.toRadians(lat2);
        double a = Math.sin(dLat/2)*Math.sin(dLat/2) +
                   Math.cos(rLat1)*Math.cos(rLat2)*
                   Math.sin(dLon/2)*Math.sin(dLon/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }
}

class Graph {
    private final Map<Node, List<Edge>> adj = new HashMap<>();
    public void addNode(Node n) {
        adj.putIfAbsent(n, new ArrayList<>());
    }
    public void addUndirectedEdge(Node a, Node b) {
        addNode(a);
        addNode(b);
        Edge ab = new Edge(a, b);
        adj.get(a).add(ab);
        Edge ba = new Edge(b, a);
        adj.get(b).add(ba);
    }
    public List<Node> shortestPath(Node start, Node goal) {
        Map<Node, Double> dist = new HashMap<>();
        Map<Node, Node> prev = new HashMap<>();
        PriorityQueue<Node> pq = new PriorityQueue<>(Comparator.comparingDouble(dist::get));
        for(Node n : adj.keySet()) {
            dist.put(n, Double.POSITIVE_INFINITY);
        }
        dist.put(start, 0.0);
        pq.add(start);
        while(!pq.isEmpty()) {
            Node u = pq.poll();
            if(u.equals(goal)) break;
            for(Edge e : adj.get(u)) {
                double alt = dist.get(u) + e.weight;
                if(alt < dist.get(e.to)) {
                    dist.put(e.to, alt);
                    prev.put(e.to, u);
                    pq.remove(e.to);
                    pq.add(e.to);
                }
            }
        }
        // reconstruct path
        LinkedList<Node> path = new LinkedList<>();
        for(Node at = goal; at != null; at = prev.get(at)) {
            path.addFirst(at);
        }
        if(path.isEmpty() || !path.getFirst().equals(start)) return Collections.emptyList();
        return path;
    }
}

public class ShortestPath {
    public static void main(String[] args) {
        // Demo with two road signs: Gaehwa JC -> Incheon Airport
        Node gaehwaSign = new Node("GAE_JC", new GeoPosition(37.5699, 126.8105));
        Node incheonAirportSign = new Node("ICN_APT", new GeoPosition(37.4602, 126.4407));
        Graph g = new Graph();
        g.addUndirectedEdge(gaehwaSign, incheonAirportSign);
        List<Node> path = g.shortestPath(gaehwaSign, incheonAirportSign);
        System.out.println("Shortest path:");
        for(Node n : path) {
            System.out.println(n.id);
        }
    }
}