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
    @Override public boolean equals(Object o) {
        if(this == o) return true;
        if(!(o instanceof Node)) return false;
        Node n = (Node) o;
        return java.util.Objects.equals(id, n.id);
    }
    @Override public int hashCode() { return java.util.Objects.hash(id); }
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

// Domain model ----------------------------------------------------
enum ArrowDirection { STRAIGHT, RIGHT, LEFT, EXIT_RIGHT, EXIT_LEFT }

class AircraftInfo {
    Double speedKmh; // nullable
    String color;
    AircraftInfo(Double speedKmh, String color) {
        this.speedKmh = speedKmh;
        this.color = color;
    }
}

class Destination {
    String koName;
    String enName;
    double distanceKm;
    ArrowDirection arrow;
    AircraftInfo aircraft; // optional
    Destination(String koName, String enName, double distanceKm, ArrowDirection arrow, AircraftInfo aircraft) {
        this.koName = koName;
        this.enName = enName;
        this.distanceKm = distanceKm;
        this.arrow = arrow;
        this.aircraft = aircraft;
    }
}

class SignStyle {
    int widthMm;
    int heightMm;
    String background;
    boolean hasExitNumber;
    SignStyle(int widthMm, int heightMm, String background, boolean hasExitNumber) {
        this.widthMm = widthMm;
        this.heightMm = heightMm;
        this.background = background;
        this.hasExitNumber = hasExitNumber;
    }
}

class RoadSign {
    private String signId;
    private int laneCount;
    private java.util.List<Destination> destinations = new java.util.ArrayList<>();
    private GeoPosition gps;
    private SignStyle style;
    RoadSign(String signId, int laneCount, GeoPosition gps, SignStyle style) {
        this.signId = signId;
        this.laneCount = laneCount;
        this.gps = gps;
        this.style = style;
    }
    void addDestination(Destination d) { destinations.add(d); }
    String getSignId() { return signId; }
    GeoPosition getGps() { return gps; }
    @Override public String toString() { return signId; }
}
// ----------------------------------------------------------------

public class ShortestPath {
    public static void main(String[] args) {
        // 1. Build some road signs along the route to Incheon Airport
        RoadSign seoul = new RoadSign("SEOUL_CEN", 5,
                new GeoPosition(37.5665, 126.9780),
                new SignStyle(6000, 2800, "green", false));
        seoul.addDestination(new Destination("서울", "Seoul", -1, ArrowDirection.STRAIGHT, null));

        RoadSign gaehwa = new RoadSign("GAEHWA_JC", 3,
                new GeoPosition(37.5699, 126.8105),
                new SignStyle(6000, 2800, "green", false));
        gaehwa.addDestination(new Destination("강남·광주", "Gangnam / Gwangju", -1, ArrowDirection.RIGHT, null));

        RoadSign unseo = new RoadSign("UNSEO_IC", 3,
                new GeoPosition(37.4925, 126.4932),
                new SignStyle(6000, 2800, "green", false));
        unseo.addDestination(new Destination("운서", "Unseo", -1, ArrowDirection.STRAIGHT, null));

        RoadSign incheonAirport = new RoadSign("ICN_APT", 4,
                new GeoPosition(37.4602, 126.4407),
                new SignStyle(8000, 3000, "green", false));
        incheonAirport.addDestination(new Destination("인천공항", "Incheon Airport", 0,
                ArrowDirection.STRAIGHT,
                new AircraftInfo(900.0, "white-blue")));

        // 2. Convert to graph nodes
        Node nSeoul = new Node(seoul.getSignId(), seoul.getGps());
        Node nGaehwa = new Node(gaehwa.getSignId(), gaehwa.getGps());
        Node nUnseo = new Node(unseo.getSignId(), unseo.getGps());
        Node nAirport = new Node(incheonAirport.getSignId(), incheonAirport.getGps());

        // 3. Build graph (simple linear path for demo)
        Graph g = new Graph();
        g.addUndirectedEdge(nSeoul, nGaehwa);
        g.addUndirectedEdge(nGaehwa, nUnseo);
        g.addUndirectedEdge(nUnseo, nAirport);

        // 4. Compute shortest path
        java.util.List<Node> path = g.shortestPath(nSeoul, nAirport);
        System.out.println("=== Navigation Seoul → Incheon Airport ===");
        for(Node n : path) {
            System.out.println("• " + n.id);
        }
    }
}