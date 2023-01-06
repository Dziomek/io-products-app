const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: null,
			username: null,
			email: null,
		},
		actions: {
			syncDataFromSessionStorage: () => {
				const token = sessionStorage.getItem("token")
				const username = sessionStorage.getItem("username")
				const email = sessionStorage.getItem("email")
				
				if(token) setStore({ token: token })
				if(username) setStore({ username: username})
				if(email) setStore({ email: email })
				console.log('Store sync with sessionStorage. Token:', token,
					'username', username,
					'email', email
				)
			},
			removeStoreData: () => {
				sessionStorage.removeItem("token")
				sessionStorage.removeItem("username")
				sessionStorage.removeItem("email")
				setStore({ token: null })
				setStore({ username: null })
				setStore({ email: null })
				
			},
			login: async (token, username, email) => {
				sessionStorage.setItem("username", username)
                sessionStorage.setItem("email", email)
                sessionStorage.setItem("token", token)
				setStore({ token: token })
				setStore({ username: username })
				setStore({ email: email })
			},
			logout: () => {
				fetch("http://127.0.0.1:5000/logout")
					.then(response => {
						if(response.status === 200) {
							console.log('Logged out')
							sessionStorage.removeItem("token")
							sessionStorage.removeItem("username")
							sessionStorage.removeItem("email")
							setStore({ token: null })
							setStore({ username: null })
							setStore({ email: null })
						}
					})
			},
		}
	};
};

export default getState;