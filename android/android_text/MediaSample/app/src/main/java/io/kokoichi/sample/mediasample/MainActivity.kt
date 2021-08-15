package io.kokoichi.sample.mediasample

import android.media.MediaPlayer
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.CompoundButton
import android.widget.Switch
import java.io.IOException
import java.lang.IllegalArgumentException

class MainActivity : AppCompatActivity() {
    private var _player: MediaPlayer? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        _player = MediaPlayer()
        // 音声ファイルのURI文字列を作成
        val mediaFileUriStr = "android.resource://${packageName}/${R.raw.rain_1}"
        // 音声ファイルのURI文字列を元にURIオブジェクトを作成
        val mediaFileUri = Uri.parse(mediaFileUriStr)
        try {
            _player?.setDataSource(applicationContext, mediaFileUri)
            // 非同期でのメディア再生準備が完了した際のリスナを設定
            _player?.setOnPreparedListener(PlayerPreparedListener())
            // メディア再生が終了した際のリスナを設定
            _player?.setOnCompletionListener(PlayerCompletionListener())
            // 非同期でメディア再生を準備
            _player?.prepareAsync()
        }
        catch (ex: IllegalArgumentException) {
            Log.e("MediaSample", "メディアプレーヤー準備時の例外", ex)
        }
        catch (ex: IOException) {
            Log.e("MediaSample", "メディアプレーヤー準備時の例外", ex)
        }

        // ループスイッチ関連
        val loopSwitch = findViewById<Switch>(R.id.swLoop)
        // スイッチにリスナを設定
        loopSwitch.setOnCheckedChangeListener(LoopSwitchChangedListener())
    }

    // プレーヤーの再生準備が整った時のリスナクラス
    private inner class PlayerPreparedListener : MediaPlayer.OnPreparedListener {
        override fun onPrepared(mp: MediaPlayer?) {
            // 各ボタンをタップ可能に設定
            val btPlay = findViewById<Button>(R.id.btPlay)
            btPlay.isEnabled = true
            val btBack = findViewById<Button>(R.id.btBack)
            btBack.isEnabled = true
            val btForward = findViewById<Button>(R.id.btForward)
            btForward.isEnabled = true
        }
    }

    // 再生が終了した時のリスナクラス
    private inner class PlayerCompletionListener : MediaPlayer.OnCompletionListener {
        override fun onCompletion(mp: MediaPlayer) {
            _player?.let {
                // ループが設定されていれば
                if(!it.isLooping) {
                    // 再生ボタンのラベルを「再生」に変更
                    val btPlay = findViewById<Button>(R.id.btPlay)
                    btPlay.setText(R.string.bt_play_play)
                }
            }
        }
    }

    fun onPlayButtonClick(view: View) {
        // フィールドのプレーヤーがnullじゃなかったら
        _player?.let {
            val btPlay = findViewById<Button>(R.id.btPlay)
            // プレーヤーが再生中なら
            if(it.isPlaying) {
                // プレーヤーを一時停止。
                it.pause()
                btPlay.setText(R.string.bt_play_play)
            }
            else {
                it.start()
                btPlay.setText(R.string.bt_play_pause)
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        _player?.let {
            if(it.isPlaying) {
                it.stop()
            }
            it.release()
            _player = null
        }
    }

    fun onBackButtonClick(view: View) {
        // 再生位置を先頭に変更
        _player?.seekTo(0)
    }

    fun onForwardButtonClick(view: View) {
        _player?.let {
            // 現在再生中のメディアファイルの長さを取得
            val duration = it.duration
            it.seekTo(duration)
            if(!it.isPlaying) {
                it.start()
            }
        }
    }

    private inner class LoopSwitchChangedListener : CompoundButton.OnCheckedChangeListener {
        override fun onCheckedChanged(buttonView: CompoundButton, isChecked: Boolean) {
            // ループするかどうかを設定
            _player?.isLooping = isChecked
        }
    }
}