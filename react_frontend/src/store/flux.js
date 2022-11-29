const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: null,
			username: null
		},
		actions: {
			syncTokenFromSessionStorage: () => {
				const token = sessionStorage.getItem("token")
				const username = sessionStorage.getItem("username")
				if(token) setStore({ token: token })
				if(username) setStore({ username: username})
				console.log('Store loaded', token, username)
			},
			login: async (token, username) => {
				setStore({ token: token })
				setStore({ username: username })
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