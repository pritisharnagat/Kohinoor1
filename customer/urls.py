from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    # path('customer_base/',bootstrap_cus,name="bootstrap_cus"),
    path('view_cart/',view_cart,name="view_cart"),
    path('remove_cart/<int:id>/', remove_cart, name='remove_cart'),
    path('add_wishlist/<str:prod_id>/',add_wishlist,name="add_wishlist"),
    path('view_wishlist/',view_wishlist,name="view_wishlist"),
    path('remove_wishlist/<int:id>/',remove_wishlist,name="remove_wishlist"),

    path('prod_details/<str:prod_id>/',prod_details,name="prod_details"),
    path('add_to_cart/',add_to_cart,name="add_to_cart"),

    path('checkout/', checkout_view, name='checkout'),
    path('save_address1/', save_address1, name='save_address1'),
    path('create_order/', create_order, name='create_order'),
    path('invoice/<str:order_id>/',invoice,name="invoice"),

    path('tshirt/',tshirt,name="tshirt"),
    path('shirts/',shirts,name="shirts"),
    path('kurtas/',kurtas,name="kurtas"),
    path('sweatshirts/',sweatshirts,name="sweatshirts"),
    path('hoodies/',hoodies,name="hoodies"),
    path('quote_tshirts/',quote_tshirts,name="quote_tshirts"),
    path('Signature_tshirts/',Signature_tshirts,name="Signature_tshirts"),

    path('BR_ambedkar_quotes/',BR_ambedkar_quotes,name="BR_ambedkar_quotes"),
    path('Chrapati_shivaji_maharaj_quotes/',Chrapati_shivaji_maharaj_quotes,name="Chrapati_shivaji_maharaj_quotes"),
    path('A_P_J_Abdul_kalam_tshirts/',A_P_J_Abdul_kalam_tshirts,name="A_P_J_Abdul_kalam_tshirts"),
    path('Budha_quotes/',Budha_quotes,name="Budha_quotes"),
    path('Birsa_munda/',Birsa_munda,name="Birsa_munda"),
    path('Savitribai_Phule/',Savitribai_Phule,name="Savitribai_Phule"),
    path('Bhagat_Singh/',Bhagat_Singh,name="Bhagat_Singh"),
    path('Martin_Luther_King/',Martin_Luther_King,name="Martin_Luther_King"),
    path('Sant_Kabir_Saheb/',Sant_Kabir_Saheb,name="Sant_Kabir_Saheb"),
    path('Sri_Guru_Nanak_Dev_ji/',Sri_Guru_Nanak_Dev_ji,name="Sri_Guru_Nanak_Dev_ji"),
    path('Osho_quotes/',Osho_quotes,name="Osho_quotes"),


    path('freedomandjustice/',freedomandjustice,name="freedomandjustice"),
    path('equalityandinclusion/',equalityandinclusion,name="equalityandinclusion"),
    path('education_and_empowerment/',education_and_empowerment,name="education_and_empowerment"),

    path('Historical/',Historical,name="Historical"),
    path('modern/',modern,name="modern"),

    path('shop_by_national_region/',shop_by_national_region,name="shop_by_national_region"),
    path('shop_by_regional/',shop_by_regional,name="shop_by_regional"),

    path('shop_by_profession_education/',shop_by_profession_education,name="shop_by_profession_education"),
    path('shop_by_profession_arts/',shop_by_profession_arts,name="shop_by_profession_arts"),
    path('shop_by_profession_science/',shop_by_profession_science,name="shop_by_profession_science"),



    # clothing sub-categories t-shirts

    path('causespecifictees/',causespecifictees,name="causespecifictees"),
    path('graphictees/',graphictees,name="graphictees"),
    path('humorsatiretees/',humorsatiretees,name="humorsatiretees"),
    path('inspirationaltees/',inspirationaltees,name="inspirationaltees"),
    path('minimalisttees/',minimalisttees,name="minimalisttees"),

    # clothing sub-categories kurtas

    path('comfortwear/',comfortwear,name="comfortwear"),
    path('modernfusion/',modernfusion,name="modernfusion"),
    path('occasionwear/',occasionwear,name="occasionwear"),
    path('traditionaldesigns/',traditionaldesigns,name="traditionaldesigns"),


    # clothing sub-categories kurtas
    path('croptopsfitted/',croptopsfitted,name="croptopsfitted"),
    path('oversizedcozy/',oversizedcozy,name="oversizedcozy"),
    path('slogansweatshirts/',slogansweatshirts,name="slogansweatshirts"),
    path('zipupspullovers/',zipupspullovers,name="zipupspullovers"),




    # gifts categories
    path('gifts/',gifts,name="gifts"),
    path('themeBasedCollections/',themeBasedCollections,name="themeBasedCollections"),
    path('clothingTypeBlends/',clothingTypeBlends,name="clothingTypeBlends"),
    path('productFocusedCombinations/',productFocusedCombinations,name="productFocusedCombinations"),
    path('mixOfActivism&Education/',mixOfActivismEducation,name="mixOfActivism&Education"),

    # gits sub-categories clothingTypeBlends

    path('causespecificscarfhatcombo/',causespecificscarfhatcombo,name="causespecificscarfhatcombo"),
    path('empowermentkurtadress/',empowermentkurtadress,name="empowermentkurtadress"),
    path('statementhoodietshirtset/',statementhoodietshirtset,name="statementhoodietshirtset"),


    # gits sub-categories mixOfActivism&Education

    path('educationalresources/',educationalresources,name="educationalresources"),
    path('postersprints/',postersprints,name="postersprints"),
    path('tshirtsapparel/',tshirtsapparel,name="tshirtsapparel"),


    # gits sub-categories productFocusedCombinations
    path('activistessentialskit/',activistessentialskit,name="activistessentialskit"),
    path('ecofriendly/',ecofriendly,name="ecofriendly"),
    path('jewelrygiftbox/',jewelrygiftbox,name="jewelrygiftbox"),


    # gits sub-categories themeBasedCollections
    path('educationwarriorpack/',educationwarriorpack,name="educationwarriorpack"),
    path('equalitychampionscollection/',equalitychampionscollection,name="equalitychampionscollection"),
    path('peacepilgrimbundle/',peacepilgrimbundle,name="peacepilgrimbundle"),



    # painting categories
    path('limitededitionprints/',limitededitionprints,name="limitededitionprints"),
    path('localregionalartists/',localregionalartists,name="localregionalartists"),
    path('portraits/',portraits,name="portraits"),
    path('thematiccollections/',thematiccollections,name="thematiccollections"),



    # books
    path('books/',books,name="books"),

    #books sub-categories biographies-and-autobiographies
    path('biographiesautobiographies/',biographiesautobiographies,name="biographiesautobiographies"),


    #books sub-categories childrens-books
    path('childrensbooks/',childrensbooks,name="childrensbooks"),



    #books sub-categories fiction-and-poetry
    path('fictionandpoetry/',fictionandpoetry,name="fictionandpoetry"),



    #books sub-categories social-justice
    path('socialjusticetexts/',socialjusticetexts,name="socialjusticetexts"),


    # paintings
    path('paintings/',paintings,name="paintings"),



    # books categories
    path('biographiesandautobiographies/',biographiesandautobiographies,name="biographiesandautobiographies"),
    path('childrensbooks/',childrensbooks,name="childrensbooks"),
    path('fictionandpoetry/',fictionandpoetry,name="fictionandpoetry"),
    path('socialjustice/',socialjustice,name="socialjustice"),

    path('add_queries/',add_queries,name="add_queries"),  

    path('customization/<str:prod_id>/',customization,name="customization"),
    path('orders/',orders,name='orders'),

    path('order_tracking/<str:order_id>/', order_tracking, name='order_tracking'),

    path('cancel_order/<str:order_id>/', cancel_order, name='cancel_order'),
    path('return_order/<str:order_id>/',return_order,name='return_order'),

    path('customer_order_report/',customer_order_report,name='customer_order_report'),

    path('canceled_orders/', canceled_orders, name='canceled_orders'),

    path('customize_plane_tshirt/',customize_plane_tshirt,name='customize_plane_tshirt'),

    # path('razorpay_payment/',razorpay_payment,name='razorpay_payment'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
    path('payment_method/', payment_method, name='payment_method'),


    # blogs customers
    path('customer_blog_details/<int:id>/',customer_blog_details,name='customer_blog_details'),
    path('filter_products/<slug:data>/', filter_products, name='filter_products'),
    path('filter/', filter ,name='filter'),

    path('tshirt_male/', tshirt_male ,name='tshirt_male'),
    path('tshirt_female/', tshirt_female ,name='tshirt_female'),
    path('filter_colour/<str:data>/', filter_colour ,name='filter_colour'),

    path('filter_size/<str:size>/', filter_size ,name='filter_size'),

    path('add_cart/<str:prod_id>/', add_cart ,name='add_cart'),
    path('update_reviews/<str:prod_id>/<int:id>/',update_reviews,name="update_reviews"),

    
    #collecations filter
    path('tshirt_male_shivaji_maharaj/', collection_male ,name='tshirt_male_shivaji_maharaj'),
    path('tshirt_female_shivaji_maharaj/', tshirt_female_shivaji_maharaj ,name='tshirt_female_shivaji_maharaj'),
    path('filter_products_collection/<slug:data>/', filter_products_collection ,name='filter_products_collection'),
    path('filter_product_price/<slug:data>/', filter_product_price ,name='filter_product_price'),
    path('filter_colour_collection/<slug:data>/', filter_colour_collection ,name='filter_colour_collection'),
    path('filter_size_collection/<slug:data>/', filter_size_collection ,name='filter_size_collection'),
    path('updated_products/', updated_products ,name='updated_products'),

    path('move_to_wishlist/<str:prod_id>/', move_to_wishlist ,name='move_to_wishlist'),

    path('search/', search ,name='search'),
    
    path('create_order_api/', create_order_api ,name='create_order_api'),
    path('cancel_order_api/<str:order_id>/', cancel_order_api ,name='cancel_order_api'),


]