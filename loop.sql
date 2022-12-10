do $$
	begin
		for counter in 0..5
			loop
				if counter not in (select id_country from country) then
					insert into country (id_country, name_country)
             		values (counter, 'country_'||counter);
				else
-- 					delete from country where name_country = 'country_'||counter;
				end if;
			end loop;
	end
$$

--select * from country