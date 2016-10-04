curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type" : "call_to_actions",
  "thread_state" : "existing_thread",
  "call_to_actions":[
    {
      "type":"postback",
      "title":"繳交費用",
      "payload":"PAY_RENT"
    },
    {
      "type":"postback",
      "title":"設定銀行帳號",
      "payload":"SETTING_ACCOUNT"
    },
    {
      "type":"postback",
      "title":"調整房間費用",
      "payload":"CHANGE_ROOM_FEE"
    }
  ]
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAARbX2lVdesBAK4cLqF3M7XpRgxvqsasZCF4fHMStvM0xnEez9tq77ES1FIx4mjfwvXq8aJJGReJleGnbfpdAQwBHGoAr6HbIeNzwy6IaKdOq3fAXed2ZCjZCwOwCeBeyX6I0rJj0RDXb6sJVmhSZA6DzQbpACoseH5EMc9kswZDZD"    


curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type":"call_to_actions",
  "thread_state":"new_thread",
  "call_to_actions":[
    {
      "payload":"START_USE"
    }
  ]
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAARbX2lVdesBAK4cLqF3M7XpRgxvqsasZCF4fHMStvM0xnEez9tq77ES1FIx4mjfwvXq8aJJGReJleGnbfpdAQwBHGoAr6HbIeNzwy6IaKdOq3fAXed2ZCjZCwOwCeBeyX6I0rJj0RDXb6sJVmhSZA6DzQbpACoseH5EMc9kswZDZD"
