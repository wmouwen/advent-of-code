import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

class Asteroid
{
    int x, y;
    HashMap<Long, Asteroid> visible;

    public Asteroid(int x, int y)
    {
        this.x = x;
        this.y = y;
    }

    public double angle(Asteroid other)
    {
        return Math.atan2(this.x - other.x, this.y - other.y);
    }

    public long angleKey(Asteroid other)
    {
        return Math.round(100000000 * this.angle(other));
    }

    public double distance(Asteroid other)
    {
        return Math.sqrt(Math.pow(this.y - other.y, 2) + Math.pow(this.x - other.x, 2));
    }
}

public class solution
{
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args)
    {
        ArrayList<Asteroid> asteroids = new ArrayList<>();

        for (int y = 0; sc.hasNextLine(); y++) {
            char[] line = sc.nextLine().trim().toCharArray();
            for (int x = 0; x < line.length; x++) {
                if (line[x] == '#') {
                    asteroids.add(new Asteroid(x, y));
                }
            }
        }

        solution.fillVisibilityMaps(asteroids);

        Asteroid stationCandidate = null;
        for (Asteroid asteroid : asteroids) {
            if (stationCandidate == null || asteroid.visible.size() > stationCandidate.visible.size()) {
                stationCandidate = asteroid;
            }
        }
        assert stationCandidate != null;
        Asteroid station = stationCandidate;
        System.out.println(station.visible.size());

        int togo = 200;
        while (true) {
            solution.fillVisibilityMaps(asteroids);

            ArrayList<Asteroid> targets = new ArrayList<>(station.visible.values());
            targets.sort((s1, s2) -> -Double.compare(s1.angle(station), s2.angle(station)));

            for (Asteroid target : targets) {
                if (--togo == 0) {
                    System.out.println(target.x * 100 + target.y);
                    return;
                }
                asteroids.remove(target);
            }
        }
    }

    public static void fillVisibilityMaps(ArrayList<Asteroid> asteroids)
    {
        for (Asteroid asteroid : asteroids) {
            asteroid.visible = new HashMap<>();

            for (Asteroid candidate : asteroids) {
                if (asteroid.equals(candidate)) {
                    continue;
                }

                long angleKey = asteroid.angleKey(candidate);
                if (asteroid.visible.containsKey(angleKey)) {
                    if (asteroid.distance(candidate) < asteroid.distance(asteroid.visible.get(angleKey))) {
                        asteroid.visible.replace(angleKey, candidate);
                    }

                } else {
                    asteroid.visible.put(angleKey, candidate);
                }
            }
        }
    }
}
