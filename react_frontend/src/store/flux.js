const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: null,
			username: null,
			email: null,
			id: null,
		},
		actions: {
			syncDataFromSessionStorage: () => {
				const token = sessionStorage.getItem("token")
				const username = sessionStorage.getItem("username")
				const email = sessionStorage.getItem("email")
				const id = sessionStorage.getItem("id")
				
				if(token) setStore({ token: token })
				if(username) setStore({ username: username})
				if(email) setStore({ email: email })
				if(id) setStore({ id: id })
				console.log('Store sync with sessionStorage. Token:', token,
					'username', username,
					'email', email,
					'id', id
				)
			},
			removeStoreData: () => {
				sessionStorage.removeItem("token")
				sessionStorage.removeItem("username")
				sessionStorage.removeItem("email")
				sessionStorage.removeItem("id")			
				setStore({ token: null })
				setStore({ username: null })
				setStore({ email: null })
				setStore({ id: null })
				
			},
			login: async (token, username, email, id) => {
				sessionStorage.setItem("username", username)
                sessionStorage.setItem("email", email)
                sessionStorage.setItem("token", token)
				sessionStorage.setItem("id", id)
				setStore({ token: token })
				setStore({ username: username })
				setStore({ email: email })
				setStore({ id: id })
			},
			logout: () => {
				fetch("http://127.0.0.1:5000/logout")
					.then(response => {
						if(response.status === 200) {
							console.log('Logged out')
							sessionStorage.removeItem("token")
							sessionStorage.removeItem("username")
							sessionStorage.removeItem("email")
							sessionStorage.removeItem("id")
							setStore({ token: null })
							setStore({ username: null })
							setStore({ email: null })
							setStore({ id: null })
						}
					})
			},
		}
	};
};

export default getState;