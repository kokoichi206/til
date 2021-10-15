INSERT INTO member_infos (member_id, birthday, blood_type, height, generation, blog_url, img_url)
	 VALUES (1, '3月12日', 'X', '199', '3期生', 
     'https://hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=23',
     'https://firebasestorage.googleapis.com/v0/b/my-memory-3b3bd.appspot.com/o/saka%2Fhinatazaka%2Fmorimotomarii.jpeg?alt=media');

select * from member_infos where height > '160cm';

