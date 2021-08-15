package io.kokoichi.sample.implicitintentsample

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.EditText
import android.widget.TextView
import androidx.core.app.ActivityCompat
import java.net.URLEncoder

class MainActivity : AppCompatActivity() {
    // 緯度フィールド
    private var _latitude = 35.64
    // 経度フィールド
    private var _longitude = 139.75

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // GPS機能を利用し、現在地
        // からINFOを受け取る
        val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        // 位置情報が更新された際のリスナオブジェクトを作成
        val locationListener = GPSLocationListener()
        // 位置情報の追跡を開始
        if (ActivityCompat.checkSelfPermission(
                applicationContext,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            // ACCESS_FINE_LOCATIONの許可を求めるダイアログを表示
            val permissions = arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
            ActivityCompat.requestPermissions(this@MainActivity, permissions, 1000)
            return
        }
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0f, locationListener)
    }

    private inner class GPSLocationListener : LocationListener {
        override fun onLocationChanged(location: Location) {
            // 引数のLocationオブジェクトから緯度経度を取得
            _latitude = location.latitude
            _longitude = location.longitude
            // 取得した値をTextViewに表示
            val tvLatitude = findViewById<TextView>(R.id.tvLatitude)
            tvLatitude.text = _latitude.toString()
            val tvLongitude = findViewById<TextView>(R.id.tvLongitude)
            tvLongitude.text = _longitude.toString()
        }

        override fun onStatusChanged(provider: String, status: Int, extras: Bundle) {}

        override fun onProviderEnabled(provider: String) {}

        override fun onProviderDisabled(provider: String) {}
    }

    fun onMapShowCurrentButtonClick(view: View) {
        // フィールドの緯度と経度の値を元にマップアプリと連携するURI文字列を生成
        val uriStr = "geo:${_latitude},${_longitude}"
        Log.d("uriobject", uriStr)
        // URI文字列からURIオブジェクトを生成
        val uri = Uri.parse(uriStr)
        // Intentオブジェクトを作成
        val intent = Intent(Intent.ACTION_VIEW, uri)
        // アクティビティを起動
        startActivity(intent)
    }

    fun onMapSearchButtonClick(view: View) {
        val etSearchWord = findViewById<EditText>(R.id.etSearchWord)
        var searchWord = etSearchWord.text.toString()
        // 入力されたキーワードをURLエンコード
        searchWord = URLEncoder.encode(searchWord, "UTF-8")
        // マッチアプリと連携するURI文字列を生成
        val uriStr = "geo:0,0?q=${searchWord}"
        // URI文字列からURIオブジェクトを生成
        val uri = Uri.parse(uriStr)
        // Intentオブジェクトを作成
        val intent = Intent(Intent.ACTION_VIEW, uri)
        // アクティビティを起動
        startActivity(intent)
    }
}