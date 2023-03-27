package com.example.applsm;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ActivityOptions;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Pair;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

public class MainActivity extends AppCompatActivity {

    Animation topAnimation, bottonAnimation;
    ImageView img_izquierda, img_derecha;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        img_derecha = findViewById(R.id.imgDerecha);
        img_izquierda = findViewById(R.id.imgIzquierda);

        //Animaciones
        topAnimation = AnimationUtils.loadAnimation(this, R.anim.top_animation);
        bottonAnimation = AnimationUtils.loadAnimation(this, R.anim.botton_animation);

        img_izquierda.setAnimation(topAnimation);
        img_derecha.setAnimation(bottonAnimation);

        int SPLASH_SCREEN = 3000;
        new Handler().postDelayed(() -> {
            Intent intent = new Intent(MainActivity.this, Camara.class);
            @SuppressWarnings("Unchecked")

            Pair[] pairs = new Pair[2];
            pairs[0] = new Pair<View, String>(img_izquierda, "imagen_izquierda");
            pairs[1] = new Pair<View,String>(img_derecha, "imagen_derecha");

            ActivityOptions options = ActivityOptions.makeSceneTransitionAnimation(this, pairs);
            startActivity(intent, options.toBundle());
        }, SPLASH_SCREEN);
    }
}