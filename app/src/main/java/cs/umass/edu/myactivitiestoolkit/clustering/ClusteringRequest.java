package cs.umass.edu.myactivitiestoolkit.clustering;

import org.json.JSONException;
import org.json.JSONObject;

import cs.umass.edu.myactivitiestoolkit.location.GPSLocation;
import edu.umass.cs.MHLClient.sensors.SensorReading;

/**
 * Wraps a clustering request which will be sent to the server in order to notify
 * your Python script which algorithm you would like to perform.
 *
 * @author CS390MB
 *
 * @see SensorReading
 */
public class ClusteringRequest extends SensorReading {

    /** The clustering algorithm. **/
    private final String algorithm;

    /** The clustering parameter set. **/
    private final Object[] params;

    /**
     * Instantiates a PPG reading.
     * @param userID a 10-byte hex string identifying the current user.
     * @param deviceType describes the device.
     * @param deviceID unique device identifier.
     * @param t the timestamp at which the event occurred, in Unix time by convention.
     * @param algorithm the clustering algorithm.
     */
    public ClusteringRequest(String userID, String deviceType, String deviceID, long t, String algorithm, Object... params){
        super(userID, deviceType, deviceID, "SENSOR_CLUSTERING_REQUEST", t);

        this.algorithm = algorithm;
        this.params = params;
    }

    @Override
    protected JSONObject toJSONObject(){
        JSONObject obj = getBaseJSONObject();
        JSONObject data = new JSONObject();

        try {
            data.put("t", timestamp);
            data.put("algorithm", algorithm);
            data.put("parameters", params);

            obj.put("data", data);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        return obj;
    }
}
