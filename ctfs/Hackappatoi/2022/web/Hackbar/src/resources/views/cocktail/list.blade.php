@extends('layout')

@section('content')
<div class="container">
	<div class="row">
		<div class="col-12 text-center pt-5">
			<h1 class="display-one m-5">Cocktail Recipes</h1>
			@if(session()->get('success') == 'true')
			<div class="row mt-2">
					<div class="control-group col-12 text-center alert alert-success" role="alert">
						Recipe Deleted Successfully
					</div>
			</div>
			@endif()
			<div class="text-left"><a href="cocktail/create" class="btn btn-outline-primary">Add new
				cocktail</a></div>

			<table class="table mt-3  text-left">
				<thead>
					<tr>
						<th scope="col">Cocktail Name</th>
						<th scope="col" class="pr-5">Recipe</th>
					</tr>
				</thead>
				<tbody>
					@forelse($cocktails as $cocktail)
					<tr>
						<td>{{ $cocktail->name }}</td>
						<td>{{ $cocktail->recipe }}</td>
						<td><a href="cocktail/{{ $cocktail->id }}/edit"
							class="btn btn-outline-primary">Edit</a>
							<a href="cocktail/{{ $cocktail->id }}/show"
							class="btn btn-outline-success">Show</a>
							<button type="button" class="btn btn-outline-danger ml-1"
								onClick='showModel({{ $cocktail->id }})'>Delete</button></td>
					</tr>
					@empty
					<tr>
						<td colspan="3">No cocktails found</td>
					</tr>
					@endforelse
				</tbody>
			</table>
		</div>
	</div>
</div>


<div class="modal fade" id="deleteConfirmationModel" tabindex="-1" role="dialog"
	aria-labelledby="myModalLabel">
	<div class="modal-dialog" role="document">
		<div class="modal-content">
			<div class="modal-body">Are you sure to delete this record?</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" onClick="dismissModel()">Cancel</button>
				<form id="delete-frm" class="" action="" method="POST">
                    @method('DELETE')
                    @csrf
                    <button class="btn btn-danger">Delete</button>
                </form>
			</div>
		</div>
	</div>
</div>

<script>
function showModel(id) {
	var frmDelete = document.getElementById("delete-frm");
	frmDelete.action = 'cocktail/'+id;
	var confirmationModal = document.getElementById("deleteConfirmationModel");
	confirmationModal.style.display = 'block';
	confirmationModal.classList.remove('fade');
	confirmationModal.classList.add('show');
}

function dismissModel() {
	var confirmationModal = document.getElementById("deleteConfirmationModel");
	confirmationModal.style.display = 'none';
	confirmationModal.classList.remove('show');
	confirmationModal.classList.add('fade');
}
</script>
@endsection