const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: null,
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
					setStore({ token: data.access_token })
					return true
				}
				catch(error) {
					console.log('An error occured')
				}
			},
			logout: () => {
				sessionStorage.removeItem("token")
				setStore({ token: null })
			}
		}
	};
};

export default getState;