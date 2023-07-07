# mlappp
mlapp aplicación de tipo API REstful  desarrollada en python con el framework de flask que utiliza como backend sqllite. 
Es una aplicación DEMO que cuenta con tres rutas para el acceso a los endpoints del API: Login, Usuarios y Clientes. El acceso a los endpoint requiere autenticación simple (usuario/contraseña) y  esta restringido a usuarios con perfil de acceso asignado. La autorización para el acceso a los recursos se realiza validando un jwt, que   incluye en el claim la exp, aud y sub.   La firma del jwt es calculada usando Base64URL encoding HS256

La aplicación recibe métodos HTTP  GET, POST, PUT, PATCH y  DELETE.

La aplicación está en desarrollo y puede ser utilizada para propósitos de academia o servir como referencia para tu primer webservice y familiarizarte con los conceptos relacionados.
