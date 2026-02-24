from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.register_user import RegisterUserUseCase, RegisterUserDTO
from app.application.use_cases.authenticate_user import AuthenticateUserUseCase, LoginDTO
from app.application.use_cases.user_actions import AcceptTermsUseCase, VerifyAccountUseCase
from app.application.use_cases.user_management import (
    GetUserUseCase, GetAllUsersUseCase, UpdateUserUseCase, UpdateUserDTO, DeleteUserUseCase
)
from app.presentation.schemas.user_schema import UserRegisterRequest, UserResponse, UserUpdateRequest, UserLoginRequest, TokenResponse 




# Criamos o roteador para organizar as URLs
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Endpoint para registrar um novo usuário.
    Orquestra a injeção de dependências e a chamada ao Caso de Uso.
    """
    # 1. Injeção de Dependências (Montando as peças)
    repository = UserRepositoryImpl(db)
    use_case = RegisterUserUseCase(repository)
    
    # 2. Transformando a requisição web (Schema) no DTO da Aplicação
    dto = RegisterUserDTO(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        role=request.role,
        phone=request.phone
    )
    
    # 3. Executando a lógica de negócio
    try:
        user_salvo = use_case.execute(dto)
        return user_salvo
    except ValueError as e:
        # Se o Caso de Uso estourar um erro (ex: E-mail já existe),
        # nós traduzimos isso para um erro HTTP amigável para o cliente.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/", response_model=List[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os usuários cadastrados."""
    use_case = GetAllUsersUseCase(UserRepositoryImpl(db))
    return use_case.execute(skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """Busca os detalhes de um usuário específico pelo ID."""
    use_case = GetUserUseCase(UserRepositoryImpl(db))
    try:
        return use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, request: UserUpdateRequest, db: Session = Depends(get_db)):
    """Atualiza dados básicos do perfil do usuário."""
    use_case = UpdateUserUseCase(UserRepositoryImpl(db))
    dto = UpdateUserDTO(
        user_id=user_id,
        full_name=request.full_name,
        phone=request.phone
    )
    try:
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """Desativa um usuário (Soft Delete)."""
    use_case = DeleteUserUseCase(UserRepositoryImpl(db))
    try:
        use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Autentica o usuário e devolve um Token."""
    use_case = AuthenticateUserUseCase(UserRepositoryImpl(db))
    dto = LoginDTO(email=request.email, password=request.password)
    try:
        return use_case.execute(dto)
    except ValueError as e:
        # HTTP 401 é o padrão para credenciais erradas
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.patch("/{user_id}/accept-terms", status_code=status.HTTP_204_NO_CONTENT)
def accept_terms(user_id: UUID, db: Session = Depends(get_db)):
    """Registra que o usuário aceitou os Termos de Uso (LGPD)."""
    use_case = AcceptTermsUseCase(UserRepositoryImpl(db))
    try:
        use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{user_id}/verify", status_code=status.HTTP_204_NO_CONTENT)
def verify_account(user_id: UUID, db: Session = Depends(get_db)):
    """Confirma a conta (e-mail/telefone) do usuário."""
    use_case = VerifyAccountUseCase(UserRepositoryImpl(db))
    try:
        use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))