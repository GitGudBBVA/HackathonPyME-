import googlemaps
from datetime import datetime
from Levenshtein import ratio

gmaps = googlemaps.Client(key='')

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        (",", ""),
        ("!", ""),
        ("¡", ""), 
    )
    for a,b in replacements:
        s = s.replace(a,b)
    return s

df = pd.read_csv('HackatonBBVA/Final_Data_Hackathon_2022.csv')

name_company = []
address = []
rating_start1 = []
rating_start2 = []
rating_start3 = []
rating_start4 = []
rating_start5 = []
user_ratings_total = []
rating = []
# hours = []

for i in range(df.shape[0]):
    name = df['NombComp'].iloc[i]
    name_company.append(name)
    datacrud = gmaps.places(query=name)

    m = df.iloc[i]['Direccion1']+ " " +df.iloc[i]['Direccion2'] + " " +df.iloc[i]['Colonia'] + " " +df.iloc[i]['MunicipioDel'] + " " + str(df.iloc[i]['CP']) + " " +df.iloc[i]['Estado'] + " Mexico"
    m = m.lower()
    print(m)

    if datacrud['status'] == "OK":
        for i in range(len(datacrud['results'])):
            p = datacrud['results'][i]['formatted_address']
            np = normalize(p.lower())
            coincidence = ratio(m,np)

            if coincidence > 0.65:
                address.append(p)
                id_data = datacrud['results'][i]['place_id']
                data_in = gmaps.place(place_id=id_data)
                try:
                    rating.append(data_in['result']['rating'])
                    user_ratings_total.append(data_in['result']['user_ratings_total'])
                    # hours.append(data_in['result']['opening_hours'])

                    start1 = start2 = start3 = start4 = start5 = 0
                    n = 0
                    while n < len(data_in['result']['reviews']):
                        result = data_in['result']['reviews'][n]['rating']
                        if result == 1:
                            start1 += 1 
                        elif result == 2:
                            start2 += 1         
                        elif result == 3:
                            start3 += 1   
                        elif result == 4:
                            start4 += 1 
                        elif result == 5:
                            start5 += 1       
                        n = n+1

                    rating_start1.append(start1)
                    rating_start2.append(start2)
                    rating_start3.append(start3)
                    rating_start4.append(start4)
                    rating_start5.append(start5)
                except:
                    rating_start1.append(0)
                    rating_start2.append(0)
                    rating_start3.append(0)
                    rating_start4.append(0)
                    rating_start5.append(0)
                    rating.append(0)
                    user_ratings_total.append(0)
                    # hours.append('sin dato')
            else:
                address.append('sin dato')
                rating.append('sin dato')
                user_ratings_total.append('sin dato')
                # hours.append('sin dato')
                rating_start1.append('sin dato')
                rating_start2.append('sin dato')
                rating_start3.append('sin dato')
                rating_start4.append('sin dato')
                rating_start5.append('sin dato')    
                break
    else:
        address.append('sin dato')
        rating.append('sin dato')
        user_ratings_total.append('sin dato')
        # hours.append('sin dato')
        rating_start1.append('sin dato')
        rating_start2.append('sin dato')
        rating_start3.append('sin dato')
        rating_start4.append('sin dato')
        rating_start5.append('sin dato')

diccionario = {
    'name_company':name_company,
    'address':address,
    'review_one_start':rating_start1,
    'review_two_start':rating_start2,
    'review_three_start':rating_start3,
    'review_four_start':rating_start4,
    'review_five_start':rating_start5,
    'reviews_count':user_ratings_total,
    'score(start)':rating,
}

dato_diccionario = pd.DataFrame(diccionario)
data_unida = pd.concat([df,dato_diccionario])