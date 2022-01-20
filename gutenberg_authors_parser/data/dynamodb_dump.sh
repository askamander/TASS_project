echo 'book_id	author	wikipedia_link	wikidata_id	date_of_birth	date_of_death	country_of_citizenship	occupation	languages_spoken_written_or_signed	genre	field_of_work	member_of	educated_at	influenced_by' > out_data.txt
aws dynamodb scan \
    --table-name ScrapersStack-TASSResults1EAAC180-YZ5V5TY51QWF \
    --query "Items[*].[book_id.N,author.S,wikipedia_link.S,wikidata_id.S,date_of_birth.S,date_of_death.S,country_of_citizenship.S,occupation.S,languages_spoken_written_or_signed.S,genre.S,field_of_work.S,member_of.S,educated_at.S,influenced_by.S]" \
    --output text >> out_data.txt