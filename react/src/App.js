import axios from 'axios';
import React, {Component} from 'react';
import {Table, Button, Modal, ModalHeader, ModalBody, ModalFooter, Input, Label, FormGroup, } from 'reactstrap';

class App extends Component {
  state = {
    library: [], 
    newBookModal: false,
    editBookModal: false,
    newBookDate: {
      nume: '',
      an_aparitie: 1999,
      gen: '',
      rezumat: '',
      editor: '',
    },
    editBookDate: {
      id : -1,
      nume: '',
      an_aparitie: 1999,
      gen: '',
      rezumat: '',
      editor: '',
    }
  }

  componentDidMount(){
    fetch("http://127.0.0.1:501/api/library/carti", {
      method: "GET",
      mode: "no-cors",
  }).then(
    resp => {
      this.setState({
        library: resp.data,
    });
  });
  }

  // componentDidMount(){
  //   const reqHeaders = new Headers();
  //   if (reqHeaders.has('Accept')) {
  //     reqHeaders.set('Accept', 'application/json');
  //   } else {
  //     reqHeaders.append('Accept', 'application/json');
  //   }
    
  //   // const requestParams = {
  //   //   method: 'GET',
  //   //   headers: reqHeaders,
  //   // };

  //   fetch('http://127.0.0.1:5013/api/library/carti', {mode: "no-cors", method: 'GET'})
  //     .then(response => {return response.json()})
  //     .then(data => {this.setState({ library: data })})
  //     .catch(console.log);
  // }

  toggleAddBookModal(){
    this.setState({newBookModal: !this.state.newBookModal});
  }

  toggleCancelModal(){
    this.setState({newBookModal: false});
  }
  toggleEditBookModal(){
    this.setState({editBookModal: !this.state.editBookModal});
  }

  addBook(){
    // console.log(Object.assign({}, {id:21}, this.state.newBookDate));
    console.log(this.state.library)
    let { library } = this.state;
    library.push(Object.assign({}, {id: this.state.library.length + 1}, this.state.newBookDate));
    this.setState({newBookModal:false});
    // axios.post('http://127.0.0.1:5013/api/library/carti', this.state.newBookDate).then((response) => {
    //   let { library } = this.state;
    //   library.push(Object.assign({}, {id: response.data}, this.state.newBookDate));
    //   let newBookDateInit = {
    //     nume: '',
    //     an_aparitie: 1999,
    //     gen: '',
    //     rezumat: '',
    //     editor: '',
    //   };
    //   this.setState({newBookDate: newBookDateInit, newBookModal:false});
    // })
  }

  editBook(id, nume, an, gen, rezumat, editor){
    let {editBookDate} = this.state;
    editBookDate.id = id;
    editBookDate.nume = nume;
    editBookDate.an = an;
    editBookDate.gen = gen;
    editBookDate.rezumat = rezumat;
    editBookDate.editor = editor;
    axios.put('http://127.0.0.1:5013/api/library/carti/' + id, { 
      nume, an, gen, rezumat, editor
    } ).then(response => {
      this.updateLibrary();
      this.setState({editBookModal:false});
    })
  }
  saveEdit(id, nume, an, gen, rezumat, editor){
    this.setState({editBookDate:{id, nume, an, gen, rezumat, editor}});
    this.toggleEditBookModal.bind(this);
  }

  deleteBook(id){
    axios.delete('http://127.0.0.1:501/api/library/carti/'+ id).then((response) => {
      this.updateLibrary();

    });
  }

  updateLibrary(){
    fetch("http://127.0.0.1:501/api/library/carti", {
      method: "GET",
      mode: "no-cors",
  }).then(
    resp => {
      this.setState({
        library: resp.data,
    });
  });

  }
  render(){
    let lib = this.state.library.map((book) =>{
      return(
        <tr key = {book["id"]}>
        <td>{book["id"]}</td>
        <td>{book["nume"]}</td>
        <td>{book["an_aparitie"]}</td>
        <td>{book["gen"]}</td>
        <td>{book["rezumat"]}</td>
        <td>{book["editor"]}</td>
        <td>
          <Button color = "info" size = "sm" className = "mr-2" onClick = {
            this.editBook.bind(this, book["id"], book["nume"], book["an_aparitie"], book["gen"], book["rezumat"], book["editor"])}>Edit</Button>
          <Button color = "danger" size = "sm" onClick = {this.deleteBook.bind(this, book["id"])}>DELETE</Button>
        </td>
      </tr>
      )
    })
    return (
      <div className="App container">
        <Button className = "mr-3" color="primary" onClick={this.toggleAddBookModal.bind(this)}>Adauga carte</Button>
      <Modal isOpen={this.state.newBookModal} toggle={this.toggleAddBookModal.bind(this)}>
        <ModalHeader toggle={this.toggleAddBookModal.bind(this)}>Creaza-ti propria biblioteca</ModalHeader>
        <ModalBody>
          <FormGroup>
            <Label for = "title">Titlul</Label>
            <Input id = "title" value = {this.state.newBookDate.nume} onChange = {(e) => {
              let {newBookDate} = this.state;
              newBookDate.nume = e.target.value;
              this.setState({ newBookDate })}}/>
          </FormGroup>
          <FormGroup>
            <Label for = "gen">Gen</Label>
            <Input id = "gen" value = {this.state.newBookDate.gen} onChange = {(e) => {
              let {newBookDate} = this.state;
              newBookDate.gen = e.target.value;
              this.setState({ newBookDate })}}/>
          </FormGroup>
          <FormGroup>
            <Label for = "an">Anul aparitiei</Label>
            <Input id = "an" value = {this.state.newBookDate.an_aparitie} onChange = {(e) => {
              let {newBookDate} = this.state;
              newBookDate.an_aparitie = e.target.value;
              this.setState({ newBookDate })}}/>
          </FormGroup>
          <FormGroup>
            <Label for = "rezumat">Scurt rezumat</Label>
            <Input id = "rezumat" value = {this.state.newBookDate.rezumat} onChange = {(e) => {
              let {newBookDate} = this.state;
              newBookDate.rezumat = e.target.value;
              this.setState({ newBookDate })}}/>
          </FormGroup>
          <FormGroup>
            <Label for = "editor">Editor</Label>
            <Input id = "editor" value = {this.state.newBookDate.editor} onChange = {(e) => {
              let {newBookDate} = this.state;
              newBookDate.editor = e.target.value;
              this.setState({ newBookDate })}}/>
          </FormGroup>
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.addBook.bind(this)}>Adauga</Button>{' '}
          <Button color="secondary" onClick={this.toggleCancelModal.bind(this)}>Anuleaza</Button>
        </ModalFooter>
      </Modal>

      <Modal isOpen={this.state.editBookModal} toggle={this.toggleEditBookModal.bind(this)}>
        <ModalHeader toggle={this.toggleEditBookModal.bind(this)}>Editeaza o carte</ModalHeader>
        <ModalBody>
          <FormGroup>
            <Label for = "title">Titlul</Label>
            <Input id = "title" value = {this.state.editBookDate.nume} onChange = {(e) => {
              let {editBookDate} = this.state;
              editBookDate.nume = e.target.value;
              this.setState({ editBookDate })}}/>
          </FormGroup>
          <FormGroup>
            <Label for = "gen">Gen</Label>
            <Input id = "gen" value = {this.state.editBookDate.gen} onChange = {(e) => {
              let {editBookDate} = this.state;
              editBookDate.gen = e.target.value;
              this.setState({ editBookDate })}}/>
          </FormGroup>
          <FormGroup>
            <Label for = "an">Anul aparitiei</Label>
            <Input id = "an" value = {this.state.editBookDate.an_aparitie} onChange = {(e) => {
              let {editBookDate} = this.state;
              editBookDate.an_aparitie = e.target.value;
              this.setState({ editBookDate })}}/>
          </FormGroup>
          <FormGroup>
            <Label for = "rezumat">Scurt rezumat</Label>
            <Input id = "rezumat" value = {this.state.editBookDate.rezumat} onChange = {(e) => {
              let {editBookDate} = this.state;
              editBookDate.rezumat = e.target.value;
              this.setState({ editBookDate })}}/>
          </FormGroup>
          <FormGroup>
            <Label for = "editor">Editor</Label>
            <Input id = "editor" value = {this.state.editBookDate.editor} onChange = {(e) => {
              let {editBookDate} = this.state;
              editBookDate.editor = e.target.value;
              this.setState({ editBookDate })}}/>
          </FormGroup>
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.editBook.bind(this)}>Salveaza</Button>{' '}
          <Button color="secondary" onClick={this.toggleEditBookModal.bind(this)}>Anuleaza</Button>
        </ModalFooter>
      </Modal>

        <Table>
          <thead>
            <tr>
              <th>#</th>
              <th>Nume</th>
              <th>Gen</th>
              <th>An aparitie</th>
              <th>Rezumat</th>
              <th>Editor</th>
              <th>Actiune</th>
            </tr>
          </thead>

          <tbody>
            {lib}
          </tbody>
        </Table>
      </div>
    );
  }
}

export default App;
