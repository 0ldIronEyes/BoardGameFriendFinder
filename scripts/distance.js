const API_KEY= "AIzaSyBgMTRBvh9AE3_WRD_z-htK-rlgRAtDadI";

const input = document.querySelector('#searchinput');
const suggestions = document.querySelector('.suggestions ul');
const userList = document.querySelector('.list-group')



async function calculateDistance( origin, destination) {
	var origin = '302 2nd Ave W Seattle WA 98119';
	var destination = 'New%20York%20City%2C%20NY';
	var origin_formatted = origin.replace(' ', '+');
	$.ajax({
		type: 'POST',
		url: '/calculate_distance',
		data: {origin: origin_formatted, destination: destination},
		success: function(response) {
			if ('distance' in response) {
				return response.distance;
			} else {
				return 'unknown distance away';
			}
		},
		error: function() {
			return 'unknown distance away';
		}
	});
}
