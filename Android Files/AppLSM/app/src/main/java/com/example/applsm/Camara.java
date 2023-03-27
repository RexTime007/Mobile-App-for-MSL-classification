package com.example.applsm;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import android.content.ContentResolver;
import android.content.Intent;
import android.content.res.AssetFileDescriptor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okio.BufferedSink;
import okio.Okio;

public class Camara extends AppCompatActivity {
    CardView cardCamera;

    private static final int VIDEO_TIME = 4;
    OkHttpClient okHttpClient;
    String URL = "http://192.168.1.68:"+5000+"/upload";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camara);

        okHttpClient = new OkHttpClient();

        cardCamera = findViewById(R.id.cardCamera);

        cardCamera.setOnClickListener(v ->{
            Intent intent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
            intent.putExtra(MediaStore.EXTRA_DURATION_LIMIT, VIDEO_TIME);

            camaraLauncher.launch(intent);
        });
    }

    ActivityResultLauncher<Intent> camaraLauncher = registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
        if (result.getResultCode() == RESULT_OK){
            try {
                sendVideo(result.getData().getData());
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        }
    });

    public void sendVideo(Uri uri) throws FileNotFoundException {
        ContentResolver contentResolver = getApplicationContext().getContentResolver();
        final String contentType = contentResolver.getType(uri);
        final AssetFileDescriptor fd = contentResolver.openAssetFileDescriptor(uri, "r");
        RequestBody requestBody = new RequestBody() {
            @Nullable
            @Override
            public MediaType contentType() {
                return MediaType.parse(contentType);
            }

            @Override
            public void writeTo(@NonNull BufferedSink bufferedSink) throws IOException {
                try (InputStream is = fd.createInputStream()) {
                    bufferedSink.writeAll(Okio.buffer(Okio.source(is)));
                }
            }
        };

        RequestBody multi = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file","video.mp4",requestBody)
                .build();

        Request request = new Request.Builder()
                .url(URL)
                .post(multi)
                .build();


        OkHttpClient client = new OkHttpClient.Builder()
                .readTimeout(50, TimeUnit.SECONDS)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {

            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                String r =response.body().string();
                try {resp.setText(r);}
                catch (Exception e){
                    resp.setText(e.toString());
                }
            }
        });
    }
}