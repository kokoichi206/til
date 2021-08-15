package io.kokoichi.sample.cameraintentsample

import android.Manifest
import android.content.ContentValues
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.view.View
import android.widget.ImageView
import androidx.core.app.ActivityCompat
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : AppCompatActivity() {
    // 保存された画像のURI
    private var _imageUri: Uri? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    public override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        // カメラからの戻りでかつ撮影成功の場合
        if(requestCode == 200 && resultCode == RESULT_OK) {
            // 画像を表示するImageViewを取得
            val ivCamera = findViewById<ImageView>(R.id.ivCamera)
            // フィールドの画像URIをImageViewに設定
            ivCamera.setImageURI(_imageUri)

//            // 撮影された画像のビッドマップデータを取得
//            val bitmap = data?.getParcelableExtra<Bitmap>("data")
//            // 画像そ表示するImageViewを取得
//            val ivCamera = findViewById<ImageView>(R.id.ivCamera)
//            // 撮影された画像をImageViewに設定
//            ivCamera.setImageBitmap(bitmap)
        }
    }

    // 画像部分がタップされた時の処理メソッド
    fun onCameraImageClick(view: View) {
        // WRITE_EXTERNAL_STORAGEの許可が降りていないなら
        if(ActivityCompat.checkSelfPermission(this, Manifest.permission.
            WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            val permissions = arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE)
            ActivityCompat.requestPermissions(this, permissions, 2000)
            return
        }

        val dateFormat = SimpleDateFormat("yyyyMMddHHmmss")
        val now = Date()
        val nowStr = dateFormat.format(now)
        // ストレージに格納する画像のファイル名を生成。
        val fileName = "UseCameraActivityPhoto_${nowStr}.jpg"

        // ContentValuesオブジェクトを作成
        val values = ContentValues()
        values.put(MediaStore.Images.Media.TITLE, fileName)
        values.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")

        // ContentResolverを使ってURIオブジェクトを生成
        _imageUri = contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)
        // Intentオブジェクトを作成
        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        // Extraj応報として_imageUriを設定
        intent.putExtra(MediaStore.EXTRA_OUTPUT, _imageUri)
        // アクティビティを起動
        startActivityForResult(intent, 200)

//        // ただのカメラ起動モード
//        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
//        startActivityForResult(intent, 200)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        if(requestCode == 2000 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            // 許可後にもう一度カメラアプリを起動
            val ivCamera = findViewById<ImageView>(R.id.ivCamera)
            onCameraImageClick(ivCamera)
        }
    }
}