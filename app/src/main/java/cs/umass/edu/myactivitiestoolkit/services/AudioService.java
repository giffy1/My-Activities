package cs.umass.edu.myactivitiestoolkit.services;

import android.content.Intent;
import android.support.v4.content.LocalBroadcastManager;
import android.util.Log;

import org.imirsel.m2k.util.Window;
import org.json.JSONException;
import org.json.JSONObject;

import at.tuwien.ifs.feature.extraction.audio.spectrum.Spectrogram;
import cs.umass.edu.myactivitiestoolkit.R;
import cs.umass.edu.myactivitiestoolkit.audio.AudioBufferReading;
import cs.umass.edu.myactivitiestoolkit.audio.MicrophoneRecorder;
import cs.umass.edu.myactivitiestoolkit.constants.Constants;
import cs.umass.edu.myactivitiestoolkit.view.fragments.AudioFragment;
import edu.umass.cs.MHLClient.client.MessageReceiver;

/**
 * The audio service records audio data from the microphone. Data is recorded at 8 kHz, meaning
 * each second, you will receive a buffer of 8000 samples. We have set the service up to compute
 * the spectrogram of the audio data for you and send it to the UI for visualization.
 * <br><br>
 *
 * Assignment 4 : In this assignment, you will send the incoming audio buffer to the server.
 * In your Python script, you will do the entire processing and classification pipeline. In
 * {@link #onConnected()}, we have registered a {@link edu.umass.cs.MHLClient.client.MessageReceiver}
 * for handling speaker identification results sent from the server. We have parsed the speaker
 * for you, but you have to  relay it to the UI. In {@link AudioFragment}, you should display
 * the result to the user in an intuitive form.
 *
 * @author CS390MB
 *
 * @see MicrophoneRecorder
 * @see MicrophoneRecorder.MicrophoneListener
 * @see AudioBufferReading
 * @see Constants.MHLClientFilter
 * @see edu.umass.cs.MHLClient.client.MessageReceiver
 * @see SensorService
 * @see android.app.Service
 * @see #mClient
 */
public class AudioService extends SensorService implements MicrophoneRecorder.MicrophoneListener {

    /** Used during debugging to identify logs by class */
    @SuppressWarnings("unused")
    private static final String TAG = AudioService.class.getName();

    /** The sensor responsible for collecting audio data from the phone. */
    private MicrophoneRecorder mMicrophoneRecorder;

    @Override
    protected void onServiceStarted() {
        broadcastMessage(Constants.MESSAGE.AUDIO_SERVICE_STARTED);
    }

    @Override
    protected void onServiceStopped() {
        broadcastMessage(Constants.MESSAGE.AUDIO_SERVICE_STOPPED);
    }

    protected void registerSensors() {
        mMicrophoneRecorder = MicrophoneRecorder.getInstance(this);

        Log.d(TAG, "Starting microphone.");
        mMicrophoneRecorder.registerListener(this);
        mMicrophoneRecorder.startRecording();

    }

    protected void unregisterSensors() {
        if (mMicrophoneRecorder != null) {
            mMicrophoneRecorder.unregisterListener(this);
            mMicrophoneRecorder.stopRecording();
        }
    }

    @Override
    public void onConnected() {
        mClient.registerMessageReceiver(new MessageReceiver(Constants.MHLClientFilter.SPEAKER_DETECTED) {
            @Override
            protected void onMessageReceived(JSONObject json) {
                String speaker;
                try {
                    JSONObject data = json.getJSONObject("data");
                    speaker = data.getString("speaker");
                } catch (JSONException e) {
                    e.printStackTrace();
                    return;
                }
                // TODO: Send the speaker to the UI
            }
        });
        super.onConnected();
    }

    @Override
    protected int getNotificationID() {
        return Constants.NOTIFICATION_ID.AUDIO_SERVICE;
    }

    @Override
    protected String getNotificationContentText() {
        return getString(R.string.audio_service_notification);
    }

    @Override
    protected int getNotificationIconResourceID() {
        return R.drawable.ic_mic_white_24dp;
    }

    /**
     * Broadcasts spectrogram of audio data.
     * @param spectrogram 2d array of values
     */
    public void broadcastSpectrogram(double[][] spectrogram) {
        Intent intent = new Intent();
        intent.putExtra(Constants.KEY.SPECTROGRAM, spectrogram);
        intent.setAction(Constants.ACTION.BROADCAST_SPECTROGRAM);
        LocalBroadcastManager manager = LocalBroadcastManager.getInstance(this);
        manager.sendBroadcast(intent);
    }

    /**
     * Called when an audio buffer is received. We compute and visualize the spectrogram
     * for you.
     * <br><br>
     *
     * Your job is just to send the audio buffer to the server. You should wrap it using
     * an {@link AudioBufferReading}. For the timestamp, you can pass in any arbitrary
     * value, or the current system time. It doesn't matter since it won't be used on the
     * other end, as we aren't live streaming the audio data.
     *
     * @param buffer the raw audio data
     * @param window_size the size of the buffer
     *
     * @see MicrophoneRecorder
     * @see cs.umass.edu.myactivitiestoolkit.audio.MicrophoneRecorder.MicrophoneListener
     * @see AudioBufferReading
     */
    @Override
    public void microphoneBuffer(short[] buffer, int window_size) {
        Log.d(TAG, String.valueOf(buffer.length));

        //TODO: Send the audio buffer to the server

        //convert short[] to double[] for computing spectrogram
        double[] dBuffer = new double[buffer.length];
        for (int j=0;j<buffer.length;j++) {
            dBuffer[j] = buffer[j];
        }

        //compute spectrogram
        double[][] spectrogram = Spectrogram.computeSpectrogram(dBuffer, 100, 50, Window.RECTANGULAR);

        //broadcast to UI
        broadcastSpectrogram(spectrogram);
    }
}
