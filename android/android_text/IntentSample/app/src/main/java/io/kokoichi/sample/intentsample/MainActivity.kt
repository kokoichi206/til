package io.kokoichi.sample.intentsample

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.ContextMenu
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.AdapterView
import android.widget.ListView
import android.widget.SimpleAdapter
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    // リストビューに表示するリストデータ
    private var _menuList: MutableList<MutableMap<String, String>>? = null
    // SimpleAdapterの第4引数fromに使用する定数フィールド
    private val FROM = arrayOf("name", "price")
    // SimpleAdapterの第5引数toに使用する定数フィールド
    private val TO = intArrayOf(R.id.tvMenuName, R.id.tvMenuPrice)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val lvMenu = findViewById<ListView>(R.id.lvMenu)
        val menuList: MutableList<MutableMap<String, String>> = mutableListOf()
        
//        var menu = mutableMapOf("name" to "からあげ定食", "price" to "800円")
//        menuList.add(menu)
//        menu = mutableMapOf("name" to "ハンバーグ定食", "price" to "850円")
////        menuList.add(menu)
//
//        val from = arrayOf("name", "price")
//        val to = intArrayOf(android.R.id.text1, android.R.id.text2)
        val adapter = SimpleAdapter(applicationContext, menuList, android.R.layout.simple_list_item_2, FROM, TO)
        // アダプタの登録
        lvMenu.adapter = adapter

        lvMenu.onItemClickListener = ListItemClickListener()

        // コンテキストメニューの追加
        registerForContextMenu(lvMenu)
    }

    override fun onContextItemSelected(item: MenuItem): Boolean {
        Log.d("my_tag", "fun onContextItemSelected: called")
        // 長押しされたビューに関する情報が格納されたオブジェクトを取得
        val info = item.menuInfo as AdapterView.AdapterContextMenuInfo
        // 長押しされたリストのポジションを取得
        val listPosition = info.position
        // ポジションから長押しされたメニュー情報Mapオブジェクトを取得
        val menu = _menuList!![listPosition]
        Log.d("my_tag", menu.javaClass.name)

        // 選択されたメニューのIDのR値による処理の分岐
        when(item.itemId) {
            R.id.menuListContextDesc -> {
                val desc = menu["desc"] as String
                // トーストを表示
                Toast.makeText(applicationContext, desc, Toast.LENGTH_LONG).show()
            }
            R.id.menuListContextOrder ->
                order(menu)
        }
        // 親クラスの同名メソッドを呼び出し、その戻り値を返却
        return super.onContextItemSelected(item)
    }

    private inner class ListItemClickListener : AdapterView.OnItemClickListener {
        override fun onItemClick(parent: AdapterView<*>, view: View, position: Int, id: Long) {
            // タップされた行のデータを取得。SimpleAdapterでは1行分のデータはMutableMap型！
            val item = parent.getItemAtPosition(position) as MutableMap<String, String>

            order(item)
        }
    }
    private fun order(menu: MutableMap<String, String>) {
        // 定食名と金額を取得
        val menuName = menu["name"]
        val menuPrice = menu["price"]
        // インテントオブジェクトを作成
        val intent = Intent(applicationContext, MenuThanksActivity::class.java)
        // 第2画面に送るデータを格納
        intent.putExtra("menuName", menuName)
        intent.putExtra("menuPrice", menuPrice)
        // 第2画面の起動
        startActivity(intent)
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // オプションメニュー用xmlファイルをインフレイト
        menuInflater.inflate(R.menu.menu_options_menu_list, menu)
        // 親クラスの同名メソッドを呼び出し、その戻り値を返却
        return super.onCreateOptionsMenu(menu)
    }

    private fun createCurryList(): MutableList<MutableMap<String, String>> {
        val menuList: MutableList<MutableMap<String, String>> = mutableListOf()
        // 「ビーフカレー」のデータを格納するMapオブジェクトの用意とmenuListへのデータ登録
        var menu = mutableMapOf("name" to "ビーフカレー", "price" to "520", "desc" to
                "特選スパイスを効かせた国産ビーフ100%のカレーです")
        menuList.add(menu)
        menu = mutableMapOf("name" to "ビーフカレー", "price" to "520", "desc" to
                "特選スパイスを効かせた国産ビーフ100%のカレーです")
        menuList.add(menu)

        return menuList
    }

    private fun createTeishokuList(): MutableList<MutableMap<String, String>> {
        val menuList: MutableList<MutableMap<String, String>> = mutableListOf()
        // 「ビーフカレー」のデータを格納するMapオブジェクトの用意とmenuListへのデータ登録
        var menu = mutableMapOf("name" to "なんとか定食", "price" to "920", "desc" to
                "定食よこれが")
        menuList.add(menu)
        menu = mutableMapOf("name" to "鰻定食", "price" to "5220", "desc" to
                "たけえよ")
        menuList.add(menu)

        return menuList
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // 選択されたメニューのIDのR値による処理の分岐
        when(item.itemId) {
            R.id.menuListOptionTeishoku ->
                _menuList = createTeishokuList()
            R.id.menuListOptionCurry ->
                _menuList = createCurryList()
        }
        // 画面部品listViewを取得
        val lvMenu = findViewById<ListView>(R.id.lvMenu)
        // SimpleAdapterを生成
        val adapter = SimpleAdapter(applicationContext, _menuList, R.layout.row, FROM, TO)
        // アダプタの登録
        lvMenu.adapter = adapter
        // 親クラスの同名メソッドを呼び出し、その戻り値を返却
        return super.onOptionsItemSelected(item)
    }

    override fun onCreateContextMenu(
        menu: ContextMenu,
        v: View,
        menuInfo: ContextMenu.ContextMenuInfo
    ) {
        super.onCreateContextMenu(menu, v, menuInfo)
        // コンテキストメニュー用xmlファイルをインフレイト
        menuInflater.inflate(R.menu.menu_context_menu_list, menu)
        // コンテキストメニューのヘッダタイトルを設定
        menu.setHeaderTitle(R.string.menu_list_context_header)
    }
}