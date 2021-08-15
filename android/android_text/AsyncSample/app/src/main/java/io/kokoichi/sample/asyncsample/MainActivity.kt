package io.kokoichi.sample.asyncsample

import android.os.AsyncTask
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.ListView
import android.widget.SimpleAdapter
import android.widget.TextView
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStream
import java.io.InputStreamReader
import java.lang.StringBuilder
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val lvCityList = findViewById<ListView>(R.id.lvCityList)
        // SimpleAdapterで使用するMutableListオブジェクトを用意
        val cityList: MutableList<MutableMap<String, String>> = mutableListOf()
        var city = mutableMapOf("name" to "大阪", "id" to "270000")
        cityList.add(city)
        city = mutableMapOf("name" to "神戸", "id" to "280010")
        cityList.add(city)
        city = mutableMapOf("name" to "東京", "id" to "130010")
        cityList.add(city)
        city = mutableMapOf("name" to "千葉", "id" to "120010")
        cityList.add(city)
        city = mutableMapOf("name" to "山口", "id" to "350020")
        cityList.add(city)
        city = mutableMapOf("name" to "京都", "id" to "260010")
        cityList.add(city)

        // SimpleAdapterで使用するfrom-to用変数の用意
        val from = arrayOf("name")
        val to = intArrayOf(android.R.id.text1)
        // SimpleAdapterを作成
        val adapter = SimpleAdapter(applicationContext, cityList,
            android.R.layout.simple_expandable_list_item_1, from, to)
        lvCityList.adapter = adapter
        // リストタップのリスなクラス登録
        lvCityList.onItemClickListener = ListItemClickListener()
    }

    // リストがタップされた時の処理が記述されたメンバクラス
    private inner class ListItemClickListener : AdapterView.OnItemClickListener {
        override fun onItemClick(parent: AdapterView<*>, view: View, position: Int, id: Long) {
            val item = parent.getItemAtPosition(position) as Map<String, String>
            val cityName = item["name"]
            val cityId = item["id"]
            // 取得したと指名をtvCityNameに設定
            val tvCityName = findViewById<TextView>(R.id.tvCityName)
            tvCityName.setText(cityName + "の天気： ")

            // WeatherInfoReceiverインスタンスを作成
            val receiver = WeatherInfoReceiver()
            receiver.execute(cityId)
        }
    }

    private inner class WeatherInfoReceiver(): AsyncTask<String, String, String>() {
        override fun doInBackground(vararg params: String): String {
            val id = params[0]
//            val urlStr = "http://weather.livedoor.com/forecast/webservice/json/v1?city=${id}"
            val urlStr = "https://weather.tsukumijima.net/api/forecast/city/${id}"
            // URLに接続する処理
            val url = URL(urlStr)
            // URLオブジェクトからHttpURLCOnnectionオブジェクトを取得
            val con = url.openConnection() as HttpURLConnection
            con.requestMethod = "GET"
            con.connect()
            // レスポンスデータを取得
            val stream = con.inputStream
            val result = is2String(stream)
            con.disconnect()
            stream.close()

            // JSON文字列を返す
            return result
        }

        override fun onPostExecute(result: String) {
            // JSON文字列からJSONObjectオブジェクトを作成
            val rootJSON = JSONObject(result)
            val descriptionJSON = rootJSON.getJSONObject("description")
            val desc = descriptionJSON.getString("text")
            val forecasts = rootJSON.getJSONArray("forecasts")
            val forecastsNow = forecasts.getJSONObject(0)
            val telop = forecastsNow.getString("telop")

            val tvWeatherTelop = findViewById<TextView>(R.id.tvWeatherTelop)
            val tvWeatherDesc = findViewById<TextView>(R.id.tvWeatherDesc)
            tvWeatherTelop.text = telop
            tvWeatherDesc.text = desc

//            tvWeatherDesc.text = result
        }

        private fun is2String(stream: InputStream): String {
            val sb = StringBuilder()
            val reader =BufferedReader(InputStreamReader(stream, "UTF-8"))
            var line = reader.readLine()
            while(line != null) {
                sb.append(line)
                line = reader.readLine()
            }
            reader.close()
            return sb.toString()
        }
    }
}