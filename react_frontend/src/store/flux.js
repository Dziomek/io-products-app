const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: null,
			username: null
		},
		actions: {
			syncTokenFromSessionStorage: () => {
				const token = sessionStorage.getItem("token")
				if(token) setStore({ token: token })
				console.log('Store loaded, token:', token)
			},
			login: async (email, password) => {
				const options = {
					method: 'POST',
					headers: {
						"Content-Type": "application/json"
					},
					body: JSON.stringify({
						email: email,
						password: password
					})
				}

				try {
					const response = await fetch("http://127.0.0.1:5000/token", options)
					if (response.status !== 200) {
						alert("An error occured")
						return false
					}
					const data = await response.json()
					sessionStorage.setItem("token", data.access_token)
					sessionStorage.setItem("username", data.username)
					setStore({ token: data.access_token })
					setStore({ username: data.username })
					return true
				}
				catch(error) {
					console.log('An error occured')
				}
			},
			logout: () => {
				fetch("http://127.0.0.1:5000/logout")
					.then(response => {
						if(response.status === 200) {
							console.log('WYLOGOWANO')
							sessionStorage.removeItem("token")
							sessionStorage.removeItem("username")
							setStore({ token: null })
							setStore({ username: null })
						}
					})
			}
		}
	};
};

export default getState;