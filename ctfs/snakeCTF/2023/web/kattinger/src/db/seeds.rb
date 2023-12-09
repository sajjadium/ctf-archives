User.create([
              { id: 1, username: 'REDACTED', password: 'REDACTEDREDACTEDREDACTED' },
              { id: 2, username: 'one', password: 'supercoolandsafepassword' },
              { id: 3, username: 'two', password: 'supercoolandsafepassword' }
            ])
Cat.create([
             { id: 1,
               description: 'A graceful cat with enchanting green eyes rests on a stair step, showcasing its adorable triangle ears and tiny visible footpad.', location: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg' },
             { id: 2,
               description: 'A stunning white cat with captivating blue eyes sits regally on a cozy perch. Its immaculate white fur is complemented by elegant grey ears, face, and tail, creating a picture of pure feline charm.', location: 'https://upload.wikimedia.org/wikipedia/commons/2/25/Siam_lilacpoint.jpg' },
             { id: 3,
               description: 'A curious cat with mesmerizing brownish-yellow eyes gazes back at you while gracefully walking away in a serene snowy landscape. The image captures the cat s enigmatic allure and its confident, independent spirit', location: 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Felis_catus-cat_on_snow.jpg/1280px-Felis_catus-cat_on_snow.jpg' },
             { id: 4,
               description: 'A captivating cat with bold black stripes fixes its gaze upon you, its enormous whiskers and eyes adding to its charismatic allure. This feline s intense presence draws you into a world of wonder and curiosity.', location: 'https://static01.nyt.com/images/2021/09/14/science/07CAT-STRIPES/07CAT-STRIPES-mediumSquareAt3X-v2.jpg' },
             { id: 5,
               description: 'A mesmerizing cat with striking green eyes and beautifully striped black and brown fur sits gracefully, its long whiskers twitching gently, against the backdrop of a charming wooden house.', location: 'https://media.4-paws.org/5/b/4/b/5b4b5a91dd9443fa1785ee7fca66850e06dcc7f9/VIER%20PFOTEN_2019-12-13_209-2890x2000-1920x1329.jpg' },
             { id: 6, description: 'This one is mine. It s grey and really cuddly :)', location: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4PPPpQeXiWIC8_mV7P9u-tb6WACxsGGJ9Ow&usqp=CAU' }
           ])
Comment.create([
                 { cat_id: 1, user_id: 2, rate: 7, body: 'I like this one' },
                 { cat_id: 2, user_id: 3, rate: 8, body: 'WOW' },
                 { cat_id: 2, user_id: 2, rate: 7, body: 'I love this one!!!!' },
                 { cat_id: 3, user_id: 3, rate: 7, body: 'Love the fur :)' },
                 { cat_id: 3, user_id: 2, rate: 9, body: 'AMAZING CAT!' },
                 { cat_id: 4, user_id: 3, rate: 3, body: 'Lovely!' },
                 { cat_id: 4, user_id: 2, rate: 8, body: 'Then why did you give only three stars?' },
                 { cat_id: 5, user_id: 3, rate: 6, body: 'cute c:' },
                 { cat_id: 6, user_id: 2, rate: 10, body: '<3' }
               ])

