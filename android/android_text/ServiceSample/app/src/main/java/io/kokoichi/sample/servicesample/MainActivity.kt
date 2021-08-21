package io.kokoichi.sample.servicesample

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button

class MainActivity : AppCompatAct
ivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // 通知からアクティビティが起動された場合
        val fromNotification = intent.getBooleanExtra("fromNotification", false)
        if(fromNotification) {
            val btPlay = findViewById<Button>(R.id.btPlay)
            val btStop = findViewById<Button>(R.id.btStop)
            btPlay.isEnabled = false
            btStop.isEnabled = true
        }
    }

    fun onPlayButtonClick(view: View) {
        // インテントオブジェクトを作成
        val intent = Intent(applicationContext, SoundManageService::class.java)
        // サービスを起動
        startService(intent)
        // 再生ボタンをタップ不可に、停止ボタンをタップ可に
        val btPlay = findViewById<Button>(R.id.btPlay)
        val btStop = findViewById<Button>(R.id.btStop)
        btPlay.isEnabled = false
        btStop.isEnabled = true
    }

    fun onStopButtonClick(view: View) {
        val intent = Intent(applicationContext, SoundManageService::class.java)
        // サービスを停止
        stopService(intent)
        val btPlay = findViewById<Button>(R.id.btPlay)
        val btStop = findViewById<Button>(R.id.btStop)
        btPlay.isEnabled = true
        btStop.isEnabled = false
    }
}