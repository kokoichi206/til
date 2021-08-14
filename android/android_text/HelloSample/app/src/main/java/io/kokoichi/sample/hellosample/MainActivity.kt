package io.kokoichi.sample.hellosample

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.*

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val btClick = findViewById<Button>(R.id.btClick)
        // リスナクラスのインスタンスを作成
        val listener = HelloListener()
        // リスナ設定メソッドでリスナを登録。
        btClick.setOnClickListener(listener)

        // クリアボタンのリスナー追加
        val btClear = findViewById<Button>(R.id.btClear)
        btClick.setOnClickListener(listener)

        // For 定食メニュー
        val lvMenu0 = findViewById<ListView>(R.id.lvMenu0)
        lvMenu0.onItemClickListener = ListItemClickListener()

        val lvMenu = findViewById<ListView>(R.id.lvMenu)
        var menuList = mutableListOf("からあげ定食","ハンバーグ定食","生姜焼き定食")
        // アダプタオブジェクトを生成
        val adapter = ArrayAdapter(applicationContext, android.R.layout.simple_list_item_1, menuList)
        lvMenu.adapter = adapter
        lvMenu.onItemClickListener = ListItemClickListenerForDialog()
    }

    private inner class ListItemClickListenerForDialog : AdapterView.OnItemClickListener {
        override fun onItemClick(parent: AdapterView<*>, view: View?, position: Int, id: Long) {
            // 注文確認ダイアログフラグメントオブジェクトを作成
            val dialogFragment = OrderConfirmDialogFragment()
            // ダイアログ表示
            dialogFragment.show(supportFragmentManager, "OrderConfirmDialogFragment")
        }
    }

    // リストがタップされた時の処理が記述されたメンバクラス
    private inner class ListItemClickListener : AdapterView.OnItemClickListener {
        override fun onItemClick(parent: AdapterView<*>, view: View?, position: Int, id: Long) {
            // どういう文法？
            val item = parent.getItemAtPosition(position) as String
            val show = "あなたが選んだ定食：" + item
            // トーストの表示
            Toast.makeText(applicationContext, show, Toast.LENGTH_LONG).show()
        }
    }

    // ボタンをクリックした時のリスナークラス
    private inner class HelloListener : View.OnClickListener {
        // OnClickListenerの中のonClickメソッドって冗長じゃない？
        override fun onClick(view: View) {
            val input = findViewById<EditText>(R.id.etName)
            val output = findViewById<TextView>(R.id.tvOutput)

            // idのR値に応じて処理を分岐
            when(view.id) {
                // 表示ボタンの場合
                R.id.btClick -> {
                    val inputStr = input.text.toString()
                    output.text = inputStr + "さん、こんにちは！"
                }
                // クリアボタンの場合
                R.id.btClear -> {
                    input.setText("")
                    output.text = ""
                }
            }
        }
    }
}