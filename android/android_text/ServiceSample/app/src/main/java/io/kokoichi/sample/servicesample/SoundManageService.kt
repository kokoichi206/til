package io.kokoichi.sample.servicesample

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.media.MediaPlayer
import android.net.Uri
import android.os.IBinder
import android.util.Log
import android.view.View
import androidx.core.app.NotificationCompat
import java.io.IOException
import java.lang.IllegalArgumentException

class SoundManageService : Service() {

    private val CHANNEL_ID = "soundmanagerservice_notification_channel"
    override fun onBind(intent: Intent): IBinder {
        TODO("Return the communication channel to the service.")
    }

    // メディアプレーヤーフィールド
    private var _player: MediaPlayer? = null

    override fun onCreate() {
        // フィールドのメディアプレーヤーオブジェクトを作成
        _player = MediaPlayer()

        // 通知チャネルの設定！
        val name = getString(R.string.notification_channel_name)
        // 通知チャネルの重要どを標準に設定
        val importance = NotificationManager.IMPORTANCE_DEFAULT
        // 通知チャネルを生成
        val channel = NotificationChannel(CHANNEL_ID, name, importance)
        // NotificationManagerオブジェクトを取得
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        // 通知チャネルを設定
        manager.createNotificationChannel(channel)
    }

    override fun onStartCommand(intent: Intent, flags: Int, startId: Int): Int {
        // 音声ファイルのURI文字列を作成
        val mediaFileUriStr = "android.resource://${packageName}/${R.raw.rain_1}"
        val mediaFileUri = Uri.parse(mediaFileUriStr)
        try {
            // メディアプレーヤーに音声ファイルを指定
            _player?.setDataSource(applicationContext, mediaFileUri)
            // 非同期でのメディア再生準備が完了した際のリスなを設定
            _player?.setOnPreparedListener(PlayerPreparedListener())
            // メディア再生が終了した際のリスなを設定
            _player?.setOnCompletionListener(PlayerCompletionListener())
            // 非同期でメディア再生を準備
            _player?.prepareAsync()
        }
        catch(ex: IllegalArgumentException) {
            Log.e("ServiceSample", "メディアプレーヤー準備中の例外発生", ex)
        }
        catch(ex: IOException) {
            Log.e("ServiceSample", "メディアプレーヤー準備中の例外発生", ex)
        }

        // 定数を返す
        return Service.START_NOT_STICKY
    }

    override fun onDestroy() {
        _player?.let {
            if(it.isPlaying) {
                it.stop()
            }
            it.release()
            _player = null
        }
    }

    /**
     * メディア再生準備が完了時のリスナクラス
     */
    private inner class PlayerPreparedListener : MediaPlayer.OnPreparedListener {
        override fun onPrepared(mp: MediaPlayer) {
            mp.start()

            // Notificationを作成するBuilderクラス作成
            val builder = NotificationCompat.Builder(applicationContext, CHANNEL_ID)
            builder.setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentTitle(getString(R.string.msg_notification_title_start))
                .setContentText(getString(R.string.msg_notification_text_start))
            // 移動先Activityクラスを指定したIntentオブジェクトを作成
            val intent = Intent(applicationContext, MainActivity::class.java)
            intent.putExtra("fromNotification", true)
            // PendingIntentオブジェクトを取得
            val stopServiceIntent = PendingIntent.getActivity(applicationContext, 0,
                intent, PendingIntent.FLAG_CANCEL_CURRENT)
            // PendingIntentオブジェクトをビルダーに設定
            builder.setContentIntent(stopServiceIntent)
            // たっ部された通知メッセージを自動的に消去するように設定
            builder.setAutoCancel(true)
            // BuilderからNotificationオブジェクトを生成
            val notification = builder.build()
            // Notificationオブジェクトを取得
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            // 通知
            manager.notify(1, notification)
        }
    }
    /**
     * メディア再生が終了した時のリスナクラス
     */
    private inner class PlayerCompletionListener : MediaPlayer.OnCompletionListener {
        override fun onCompletion(mp: MediaPlayer) {
            // 通知を飛ばす！
            // Notificationを作成するBuilderクラス作成
            val builder = NotificationCompat.Builder(applicationContext, CHANNEL_ID)
            // 通知エリアに表示されるアイコンを設定
            builder.setSmallIcon(android.R.drawable.ic_dialog_info)
            // 通知ドロワー設定
            builder.setContentTitle(getString(R.string.msg_notification_title_finish))
                .setContentText(getString(R.string.msg_notification_text_finish))
            // BuilderからNotificationオブジェクトを生成
            val notification = builder.build()
            // NotificationManagerオブジェクトを取得
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            // 通知
            manager.notify(0, notification)

            // 自分自身を終了
            stopSelf()
        }
    }
}