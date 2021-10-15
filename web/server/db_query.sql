INSERT INTO member_infos (member_id, birthday, blood_type, height, generation, blog_url, img_url)
	 VALUES (1, '3月12日', 'X', '199', '3期生', 
     'https://hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=23',
     'https://firebasestorage.googleapis.com/v0/b/my-memory-3b3bd.appspot.com/o/saka%2Fhinatazaka%2Fmorimotomarii.jpeg?alt=media');

select * from member_infos where height > '160cm';


-- 楽曲とそのフォーメーションを取得
SELECT song_id, group_id, single, title, first_row_num, second_row_num, third_row_num
    FROM songs INNER JOIN formations
        ON songs.formation_id = formations.formation_id;

-- センター一覧取得
SELECT position_id, position, title, single, name_ja
    FROM positions 
        INNER JOIN songs
            ON positions.song_id = songs.song_id
        INNER JOIN members
            ON positions.member_id = members.member_id
    WHERE positions.is_center = true;


-- 特定のタグの人を持ってくる
SELECT member_id, name_ja, tag_name
    FROM members
        INNER JOIN member_tags
            ON members.member_id = member_tags.member_id
        INNER JOIN tags
            ON member_tags.tag_id = tags.tag_id
                WHERE tags.tag_name = 'あざとい';

